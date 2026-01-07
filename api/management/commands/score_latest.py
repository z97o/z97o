import joblib, numpy as np
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Max
from dashboard.models import NetMetric, RiskScore, Region

RF_PATH = "models_store/rf_v1.joblib"
IF_PATH = "models_store/if_v1.joblib"

class Command(BaseCommand):
    help = "Score the most recent reading per region and create RiskScore."

    def handle(self, *args, **o):
        try:
            rf = joblib.load(RF_PATH)
            ifm = joblib.load(IF_PATH)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Load model failed: {e}"))
            return

        count = 0
        for rg in Region.objects.all():
            latest = NetMetric.objects.filter(region=rg).order_by("-ts").first()
            if not latest:
                continue
            x = np.array([[latest.download_mbps, latest.upload_mbps, latest.latency_ms, latest.signal_dbm, latest.users_online]])
            prob = float(rf.predict_proba(x)[0,1])
            anom = bool(ifm.predict(x)[0] == -1)
            RiskScore.objects.update_or_create(
                region=rg, ts=latest.ts,
                defaults={"risk_prob": prob, "anomaly": anom, "model_ver": "v1"},
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Scored {count} regions"))
