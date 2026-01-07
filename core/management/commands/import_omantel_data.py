import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from dashboard.models import RegionMetrics, Tower, Complaint, GeoClimate
from datetime import datetime

def _to_date(value):
    if pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None

class Command(BaseCommand):
    help = "Import Omantel NetInsight dataset from Excel into DB."

    def add_arguments(self, parser):
        parser.add_argument("--excel", required=True, help="Path to NetInsight_Large_Detailed_Dataset.xlsx")
        parser.add_argument("--regions-sheet", default="User_Base_Usage")
        parser.add_argument("--towers-sheet", default="Infrastructure")
        parser.add_argument("--complaints-sheet", default="Customer_Complaints")
        parser.add_argument("--geo-sheet", default="Geography_Climate")
        parser.add_argument("--truncate", action="store_true", help="Delete existing rows before import")

    @transaction.atomic
    def handle(self, *args, **opts):
        path = opts["excel"]
        regions_sheet = opts["regions-sheet"]
        towers_sheet = opts["towers-sheet"]
        complaints_sheet = opts["complaints-sheet"]
        geo_sheet = opts["geo-sheet"]

        if opts["truncate"]:
            self.stdout.write("Truncating tables…")
            Complaint.objects.all().delete()
            Tower.objects.all().delete()
            RegionMetrics.objects.all().delete()
            GeoClimate.objects.all().delete()

        # Regions
        self.stdout.write(f"Importing {regions_sheet}…")
        df_r = pd.read_excel(path, sheet_name=regions_sheet)
        for _, r in df_r.iterrows():
            RegionMetrics.objects.update_or_create(
                region=str(r.get("Region")).strip(),
                defaults={
                    "residential_users": _safe_int(r.get("Residential Users")),
                    "business_users": _safe_int(r.get("Business Users")),
                    "avg_data_gb_per_day": _safe_float(r.get("Avg Data/User (GB/day)")),
                    "peak_usage_hours": _safe_str(r.get("Peak Usage Hours")),
                    "age_group_dominant": _safe_str(r.get("Age Group Dominant")),
                    "usage_pattern": _safe_str(r.get("Usage Pattern")),
                },
            )

        # Towers
        self.stdout.write(f"Importing {towers_sheet}…")
        df_t = pd.read_excel(path, sheet_name=towers_sheet)
        for _, r in df_t.iterrows():
            Tower.objects.update_or_create(
                tower_id=_safe_str(r.get("Tower ID")),
                defaults={
                    "region": _safe_str(r.get("Region")),
                    "installation_date": _to_date(r.get("Installation Date")),
                    "tower_type": _safe_str(r.get("Tower Type")),
                    "technology": _safe_str(r.get("Technology")),
                    "power_source": _safe_str(r.get("Power Source")),
                    "operational_status": _safe_str(r.get("Operational Status")),
                    "max_capacity_users": _safe_int(r.get("Max Capacity (Users)")),
                },
            )

        # Complaints
        self.stdout.write(f"Importing {complaints_sheet}…")
        df_c = pd.read_excel(path, sheet_name=complaints_sheet)
        for _, r in df_c.iterrows():
            Complaint.objects.update_or_create(
                complaint_id=_safe_str(r.get("Complaint ID")),
                defaults={
                    "date": _to_date(r.get("Date")),
                    "region": _safe_str(r.get("Region")),
                    "device_type": _safe_str(r.get("Device Type")),
                    "complaint_type": _safe_str(r.get("Complaint Type")),
                    "duration_hours": _safe_float(r.get("Duration of Issue (Hours)")),
                    "impact_level": _safe_str(r.get("Impact Level")),
                    "reported_via": _safe_str(r.get("Reported via")),
                    "status": _safe_str(r.get("Status")),
                },
            )

        # Geo/Climate
        self.stdout.write(f"Importing {geo_sheet}…")
        df_g = pd.read_excel(path, sheet_name=geo_sheet)
        for _, r in df_g.iterrows():
            GeoClimate.objects.update_or_create(
                region=_safe_str(r.get("Region")),
                defaults={
                    "terrain_type": _safe_str(r.get("Terrain Type")),
                    "avg_temp_c": _safe_float(r.get("Avg Temperature (°C)")),
                    "avg_humidity_pct": _safe_float(r.get("Avg Humidity (%)")),
                    "rainy_season_effect": _safe_str(r.get("Rainy Season Effect")),
                    "signal_interference_level": _safe_str(r.get("Signal Interference Level")),
                },
            )

        self.stdout.write(self.style.SUCCESS("✅ Import completed successfully."))

def _safe_str(x):
    if pd.isna(x): return None
    return str(x).strip()

def _safe_int(x):
    if pd.isna(x) or x == "": return None
    try: return int(float(x))
    except: return None

def _safe_float(x):
    if pd.isna(x) or x == "": return None
    try: return float(x)
    except: return None
