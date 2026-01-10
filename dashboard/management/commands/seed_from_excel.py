from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from django.apps import apps

BASE_DIR = Path(__file__).resolve().parents[3]
EXCEL_PATH = BASE_DIR / "data" / "NetInsight_Large_Detailed_Dataset.xlsx"

def model_field_names(Model):
    return {f.name for f in Model._meta.get_fields() if hasattr(f, "attname")}

def safe_str(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

def to_int(x):
    try:
        if pd.isna(x): 
            return None
        return int(float(x))
    except Exception:
        return None

def to_float(x):
    try:
        if pd.isna(x): 
            return None
        return float(x)
    except Exception:
        return None

def to_date(x):
    d = pd.to_datetime(x, errors="coerce")
    return d.date() if pd.notna(d) else None

class Command(BaseCommand):
    help = "Seed database from Excel sheets safely (won't crash if some fields differ)."

    def handle(self, *args, **options):
        if not EXCEL_PATH.exists():
            self.stdout.write(self.style.ERROR(f"Excel not found: {EXCEL_PATH}"))
            return

        xl = pd.ExcelFile(EXCEL_PATH)

        # --- Models (from your DB tables: dashboard_tower, dashboard_complaint, dashboard_datausage, dashboard_geoclimate)
        Tower = apps.get_model("dashboard", "Tower")
        Complaint = apps.get_model("dashboard", "Complaint")
        DataUsage = apps.get_model("dashboard", "DataUsage")
        GeoClimate = apps.get_model("dashboard", "GeoClimate")

        # 1) Infrastructure -> Tower
        if "Infrastructure" in xl.sheet_names and Tower.objects.count() == 0:
            df = xl.parse("Infrastructure")
            df.columns = [str(c).strip() for c in df.columns]

            allowed = model_field_names(Tower)
            objs = []
            for _, r in df.iterrows():
                data = {
                    "tower_id": safe_str(r.get("Tower ID")),
                    "region": safe_str(r.get("Region")),
                    "installation_date": to_date(r.get("Installation Date")),
                    "tower_type": safe_str(r.get("Tower Type")),
                    "technology": safe_str(r.get("Technology")),
                    "power_source": safe_str(r.get("Power Source")),
                    "operational_status": safe_str(r.get("Operational Status")),
                    "max_capacity_users": to_int(r.get("Max Capacity (Users)")),
                }
                # Keep only fields that exist in model
                data = {k: v for k, v in data.items() if k in allowed and v not in ("", None)}
                objs.append(Tower(**data))

            Tower.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded towers: {len(objs)}"))
        else:
            self.stdout.write(self.style.WARNING("Skip towers (already seeded or sheet missing)."))

        # 2) Customer_Complaints -> Complaint
        if "Customer_Complaints" in xl.sheet_names and Complaint.objects.count() == 0:
            df = xl.parse("Customer_Complaints")
            df.columns = [str(c).strip() for c in df.columns]

            allowed = model_field_names(Complaint)
            objs = []
            for _, r in df.iterrows():
                data = {
                    "complaint_id": safe_str(r.get("Complaint ID")),
                    "date": to_date(r.get("Date")),
                    "region": safe_str(r.get("Region")),
                    "device_type": safe_str(r.get("Device Type")),
                    "complaint_type": safe_str(r.get("Complaint Type")),
                    "duration_hours": to_int(r.get("Duration of Issue (Hours)")),
                    "impact_level": safe_str(r.get("Impact Level")),
                    "reported_via": safe_str(r.get("Reported via")),
                    "status": safe_str(r.get("Status")),
                }
                data = {k: v for k, v in data.items() if k in allowed and v not in ("", None)}
                objs.append(Complaint(**data))

            Complaint.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded complaints: {len(objs)}"))
        else:
            self.stdout.write(self.style.WARNING("Skip complaints (already seeded or sheet missing)."))

        # 3) User_Base_Usage -> DataUsage
        if "User_Base_Usage" in xl.sheet_names and DataUsage.objects.count() == 0:
            df = xl.parse("User_Base_Usage")
            df.columns = [str(c).strip() for c in df.columns]

            allowed = model_field_names(DataUsage)
            objs = []
            for _, r in df.iterrows():
                data = {
                    "region": safe_str(r.get("Region")),
                    "residential_users": to_int(r.get("Residential Users")),
                    "business_users": to_int(r.get("Business Users")),
                    "avg_data_per_user_gb": to_float(r.get("Avg Data/User (GB/day)")),
                    "peak_usage_hours": safe_str(r.get("Peak Usage Hours")),
                    "age_group_dominant": safe_str(r.get("Age Group Dominant")),
                    "usage_pattern": safe_str(r.get("Usage Pattern")),
                }
                data = {k: v for k, v in data.items() if k in allowed and v not in ("", None)}
                objs.append(DataUsage(**data))

            DataUsage.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded usage: {len(objs)}"))
        else:
            self.stdout.write(self.style.WARNING("Skip usage (already seeded or sheet missing)."))

        # 4) Geography_Climate -> GeoClimate
        if "Geography_Climate" in xl.sheet_names and GeoClimate.objects.count() == 0:
            df = xl.parse("Geography_Climate")
            df.columns = [str(c).strip() for c in df.columns]

            allowed = model_field_names(GeoClimate)
            objs = []
            for _, r in df.iterrows():
                data = {
                    "region": safe_str(r.get("Region")),
                    "terrain_type": safe_str(r.get("Terrain Type")),
                    "avg_temperature": to_float(r.get("Avg Temperature (°C)")),
                    "avg_humidity": to_float(r.get("Avg Humidity (%)")),
                    "rainy_season_effect": safe_str(r.get("Rainy Season Effect")),
                    "signal_interference_level": safe_str(r.get("Signal Interference Level")),
                }
                data = {k: v for k, v in data.items() if k in allowed and v not in ("", None)}
                objs.append(GeoClimate(**data))

            GeoClimate.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded climate: {len(objs)}"))
        else:
            self.stdout.write(self.style.WARNING("Skip climate (already seeded or sheet missing)."))

        self.stdout.write(self.style.SUCCESS("✅ Seed finished (safe mode)."))
