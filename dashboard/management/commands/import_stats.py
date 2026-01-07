import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Region, Outlet, MonthlyStats

class Command(BaseCommand):
    help = "Import monthly stats from CSV into MonthlyStats"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, default="data/omantel_stats.csv")

    def handle(self, *args, **opts):
        path = Path(opts["file"])
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        created, updated = 0, 0
        with path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            required = {"year","month","cash_count","reversal_count"}
            if not required.issubset(set(h.strip().lower() for h in reader.fieldnames)):
                raise CommandError(f"CSV must include headers: {required}")

            for row in reader:
                year = int(row["year"])
                month = int(row["month"])
                cash = int(float(row.get("cash_count", 0)))
                rev = int(float(row.get("reversal_count", 0)))

                region_name = (row.get("region") or "").strip() or None
                outlet_name = (row.get("outlet") or "").strip() or None
                code = (row.get("code") or "").strip()

                region = None
                outlet = None
                if region_name and region_name.lower() != "all":
                    region, _ = Region.objects.get_or_create(name=region_name)
                if outlet_name and outlet_name.lower() != "all":
                    if region is None and region_name and region_name.lower() != "all":
                        region, _ = Region.objects.get_or_create(name=region_name)
                    outlet, _ = Outlet.objects.get_or_create(
                        name=outlet_name,
                        code=code or "",
                        defaults={"region": region},
                    )
                    if outlet.region != region:
                        outlet.region = region
                        outlet.save()

                obj, is_created = MonthlyStats.objects.update_or_create(
                    year=year, month=month, region=region, outlet=outlet,
                    defaults={"cash_count": cash, "reversal_count": rev},
                )
                created += 1 if is_created else 0
                updated += 0 if is_created else 1

        self.stdout.write(self.style.SUCCESS(
            f"Imported OK. Created: {created}, Updated: {updated}"
        ))
