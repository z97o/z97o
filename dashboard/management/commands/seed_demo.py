import csv
from pathlib import Path
from django.core.management.base import BaseCommand

from dashboard.models import Tower, KPIRecord, RegionMetrics  # عدّلي الأسماء إذا مختلفة

BASE_DIR = Path(__file__).resolve().parents[3]  # يرجع لمجلد المشروع
DATA_DIR = BASE_DIR / "data"

class Command(BaseCommand):
    help = "Seed demo data on production if DB is empty."

    def handle(self, *args, **options):
        # 1) Towers
        if Tower.objects.count() == 0:
            towers_path = DATA_DIR / "towers.csv"
            if towers_path.exists():
                with open(towers_path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    objs = []
                    for r in reader:
                        # عدّلي الحقول حسب CSV/MODEL عندك
                        objs.append(Tower(
                            tower_id=r.get("tower_id") or r.get("id") or r.get("TowerID"),
                            region=r.get("region") or r.get("Region"),
                            latitude=float(r.get("latitude") or r.get("lat") or 0),
                            longitude=float(r.get("longitude") or r.get("lon") or 0),
                        ))
                    Tower.objects.bulk_create(objs, ignore_conflicts=True)
                self.stdout.write(self.style.SUCCESS("Seeded towers.csv"))

        # 2) Region metrics (اختياري)
        if RegionMetrics.objects.count() == 0:
            regions_path = DATA_DIR / "regions.csv"
            if regions_path.exists():
                with open(regions_path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    objs = []
                    for r in reader:
                        objs.append(RegionMetrics(
                            region=r.get("region") or r.get("Region"),
                            # أضيفي أي أعمدة ثانية عندك هنا
                        ))
                    RegionMetrics.objects.bulk_create(objs, ignore_conflicts=True)
                self.stdout.write(self.style.SUCCESS("Seeded regions.csv"))

        self.stdout.write(self.style.SUCCESS("Seeding finished."))
