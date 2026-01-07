from django.core.management.base import BaseCommand
import pandas as pd
from dashboard.models import Region, SignalTower

class Command(BaseCommand):
    help = "Import towers CSV with columns: tower_id,name,region,lat,lng,rsrp_dbm,tech,vendor,status"

    def add_arguments(self, p):
        p.add_argument("--file", required=True)

    def handle(self, *args, **o):
        path = o["file"]
        df = pd.read_csv(path)
        df = df.fillna("")
        created = 0
        for _, r in df.iterrows():
            region,_ = Region.objects.get_or_create(name=str(r["region"]).strip())
            obj, is_new = SignalTower.objects.update_or_create(
                tower_id=str(r["tower_id"]).strip(),
                defaults={
                    "name": str(r["name"]).strip(),
                    "region": region,
                    "lat": float(r["lat"]),
                    "lng": float(r["lng"]),
                    "rsrp_dbm": float(r["rsrp_dbm"]),
                    "tech": str(r["tech"]).strip() or "5G",
                    "vendor": str(r["vendor"]).strip(),
                    "status": str(r["status"]).strip() or "Active",
                }
            )
            created += int(is_new)
        self.stdout.write(self.style.SUCCESS(f"Imported/updated {len(df)} towers ({created} new)."))
