from django.core.management.base import BaseCommand
import pandas as pd
from dashboard.models import Region, Infrastructure, NetMetric

class Command(BaseCommand):
    help = "Import time-series metrics (CSV/Excel). Columns: ts,region,tower_id,download_mbps,upload_mbps,latency_ms,signal_dbm,users_online"

    def add_arguments(self, p):
        p.add_argument("--file", required=True)

    def handle(self, *args, **o):
        path = o["file"]
        if path.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        df = df.fillna("")
        n = 0
        for _, r in df.iterrows():
            region, _ = Region.objects.get_or_create(name=str(r["region"]).strip())
            tower = None
            tower_id = str(r.get("tower_id", "")).strip()
            if tower_id:
                tower = Infrastructure.objects.filter(tower_id=tower_id).first()
            NetMetric.objects.create(
                region=region,
                tower=tower,
                ts=pd.to_datetime(r["ts"]),
                download_mbps=float(r["download_mbps"]),
                upload_mbps=float(r["upload_mbps"]),
                latency_ms=float(r["latency_ms"]),
                signal_dbm=float(r["signal_dbm"]),
                users_online=int(r["users_online"]),
            )
            n += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {n} rows from {path}"))
