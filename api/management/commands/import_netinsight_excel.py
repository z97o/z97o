import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from dashboard.models import (
    Region, CustomerComplaint, UserBaseUsage, Infrastructure, GeographyClimate
)

SHEETS = {
    "complaints": "Customer_Complaints",
    "usage": "User_Base_Usage",
    "infra": "Infrastructure",
    "climate": "Geography_Climate",
}

def col(row, name, default=""):
    """Safe getter that handles missing/NaN cells."""
    val = row.get(name, default)
    if pd.isna(val): return default
    return val

class Command(BaseCommand):
    help = "Import all sheets from NetInsight Excel into MySQL."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Path to NetInsight Excel file")

    def get_region(self, name):
        rg = str(name).strip() or "Unknown"
        region, _ = Region.objects.get_or_create(name=rg)
        return region

    @transaction.atomic
    def handle(self, *args, **opts):
        path = opts["file"]
        self.stdout.write(self.style.NOTICE(f"📥 Loading Excel from: {path}"))

        # --- read workbook, show sheets
        try:
            xls = pd.ExcelFile(path, engine="openpyxl")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Could not open Excel: {e}"))
            self.stderr.write(self.style.ERROR("Tip: pip install openpyxl"))
            raise

        self.stdout.write(self.style.SUCCESS(f"📑 Sheets found: {', '.join(xls.sheet_names)}"))

        # ============= 1) Complaints =============
        if SHEETS["complaints"] in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=SHEETS["complaints"], engine="openpyxl")
            df = df.fillna("")
            ok = 0
            for i, row in df.iterrows():
                try:
                    region = self.get_region(col(row, "Region"))
                    CustomerComplaint.objects.update_or_create(
                        complaint_id=str(col(row, "Complaint ID")),
                        defaults=dict(
                            date=pd.to_datetime(col(row, "Date")).date(),
                            region=region,
                            device_type=str(col(row, "Device Type")),
                            complaint_type=str(col(row, "Complaint Type")),
                            duration_hours=float(col(row, "Duration of Issue (Hours)", 0) or 0),
                            impact_level=str(col(row, "Impact Level")),
                            reported_via=str(col(row, "Reported via")),
                            status=str(col(row, "Status")),
                        ),
                    )
                    ok += 1
                except Exception as e:
                    self.stderr.write(self.style.WARNING(f"Row {i} (Complaints) skipped: {e}"))
            self.stdout.write(self.style.SUCCESS(f"✅ Complaints imported: {ok}"))

        # ============= 2) User Base Usage =============
        if SHEETS["usage"] in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=SHEETS["usage"], engine="openpyxl").fillna("")
            ok = 0
            for i, row in df.iterrows():
                try:
                    region = self.get_region(col(row, "Region"))
                    UserBaseUsage.objects.update_or_create(
                        region=region,
                        defaults=dict(
                            residential_users=int(col(row, "Residential Users", 0) or 0),
                            business_users=int(col(row, "Business Users", 0) or 0),
                            avg_data_gb_per_day=float(col(row, "Avg Data/User (GB/day)", 0) or 0),
                            peak_usage_hours=str(col(row, "Peak Usage Hours")),
                            age_group=str(col(row, "Age Group")),
                            dominant_usage_pattern=str(col(row, "Dominant Usage Pattern")),
                        ),
                    )
                    ok += 1
                except Exception as e:
                    self.stderr.write(self.style.WARNING(f"Row {i} (Usage) skipped: {e}"))
            self.stdout.write(self.style.SUCCESS(f"✅ User usage imported/updated: {ok}"))

        # ============= 3) Infrastructure =============
        if SHEETS["infra"] in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=SHEETS["infra"], engine="openpyxl").fillna("")
            ok = 0
            for i, row in df.iterrows():
                try:
                    region = self.get_region(col(row, "Region"))
                    Infrastructure.objects.update_or_create(
                        tower_id=str(col(row, "Tower ID")),
                        defaults=dict(
                            region=region,
                            installation_date=pd.to_datetime(col(row, "Installation Date")).date(),
                            tower_type=str(col(row, "Tower Type")),
                            technology=str(col(row, "Technology")),
                            power_source=str(col(row, "Power Source")),
                            operational_status=str(col(row, "Operational Status")),
                            max_capacity_users=int(col(row, "Max Capacity (Users)", 0) or 0),
                        ),
                    )
                    ok += 1
                except Exception as e:
                    self.stderr.write(self.style.WARNING(f"Row {i} (Infra) skipped: {e}"))
            self.stdout.write(self.style.SUCCESS(f"✅ Infrastructure imported/updated: {ok}"))

        # ============= 4) Geography & Climate =============
        if SHEETS["climate"] in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=SHEETS["climate"], engine="openpyxl").fillna("")
            ok = 0
            for i, row in df.iterrows():
                try:
                    region = self.get_region(col(row, "Region"))
                    GeographyClimate.objects.update_or_create(
                        region=region,
                        defaults=dict(
                            terrain_type=str(col(row, "Terrain Type")),
                            avg_temperature_c=float(col(row, "Avg Temperature (°C)", 0) or 0),
                            avg_humidity_pct=float(col(row, "Avg Humidity (%)", 0) or 0),
                            rainy_season_effect=str(col(row, "Rainy Season Effect")),
                            signal_interference_level=str(col(row, "Signal Interference Level")),
                        ),
                    )
                    ok += 1
                except Exception as e:
                    self.stderr.write(self.style.WARNING(f"Row {i} (Climate) skipped: {e}"))
            self.stdout.write(self.style.SUCCESS(f"✅ Climate imported/updated: {ok}"))

        self.stdout.write(self.style.SUCCESS("🎉 All sheets processed."))
