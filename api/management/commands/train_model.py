import joblib, numpy as np
from django.core.management.base import BaseCommand
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from dashboard.models import NetMetric

RF_PATH = "models_store/rf_v1.joblib"
IF_PATH = "models_store/if_v1.joblib"

class Command(BaseCommand):
    help = "Train IsolationForest (anomaly) and RandomForest (risk) from NetMetric."

    def handle(self, *args, **o):
        qs = NetMetric.objects.all().order_by("ts")
        if not qs.exists():
            self.stdout.write(self.style.ERROR("No NetMetric data found. Import first."))
            return

        X, y = [], []
        for m in qs:
            feats = [m.download_mbps, m.upload_mbps, m.latency_ms, m.signal_dbm, m.users_online]
            X.append(feats)
            degrade = int(m.download_mbps < 20 or m.latency_ms > 80)  # simple label
            y.append(degrade)

        X = np.array(X, dtype=float)
        y = np.array(y, dtype=int)

        if_model = IsolationForest(n_estimators=200, contamination="auto", random_state=42)
        if_model.fit(X)
        joblib.dump(if_model, IF_PATH)

        rf = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)
        rf.fit(X, y)
        joblib.dump(rf, RF_PATH)

        self.stdout.write(self.style.SUCCESS(f"Saved models: {RF_PATH}, {IF_PATH}"))
