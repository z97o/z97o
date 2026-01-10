from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from django.apps import apps

BASE_DIR = Path(__file__).resolve().parents[3]
EXCEL_PATH = BASE_DIR / "data" / "NetInsight_Large_Detailed_Dataset.xlsx"

class Command(BaseCommand):
    help = "Seed demo data from Excel sheets (Infrastructure, Complaints, Usage, Geography) if DB is empty."

    def handle(self, *args, **options):
        if not EXCEL_PATH.exists():
            raise FileNotFoundError(f"Excel file not found: {EXCEL_PATH}")

        # Get models safely (no hard import)
        Tower = apps.get_model("dashboard", "Tower")
        Complaint = apps.get_model("dashboard", "Complaint")
        DataUsage = apps.get_model("dashboard", "DataUsage")
        GeoClimate = apps.get_model("dashboard", "GeoClimate")

        xl = pd.ExcelFile(EXCEL_PATH)

        # -------------------------
        # 1) Infrastructure -> Tower
        # -------------------------
        if Tower.objects.count() == 0 and "Infrastructure" in xl.sheet_names:
            df = xl.parse("Infrastructure")
            df.columns = [c.strip() for c in df.columns]

            objs = []
            for _, r in df.iterrows():
                install_date = pd.to_datetime(r.get("Installation Date"), errors="coerce")
                objs.append(
                    Tower(
                        tower_id=str(r.get("Tower ID")).strip(),
                        region=str(r.get("Region")).strip(),
                        installation_date=install_date.date() if pd.notna(install_date) else None,
                        tower_type=str(r.get("Tower Type")).strip(),
                        technology=str(r.get("Technology")).strip(),
                        power_source=str(r.get("Power Source")).strip(),
                        operational_status=str(r.get("Operational Status")).strip(),
                        max_capacity_users=int(r.get("Max Capacity (Users)")) if pd.notna(r.get("Max Capacity (Users)")) else None,
                    )
                )

            Tower.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(objs)} towers from Infrastructure sheet."))
        else:
            self.stdout.write(self.style.WARNING("Towers table already has data (or sheet missing). Skipping towers."))

        # ------------------------------
        # 2) Customer_Complaints -> Complaint
        # ------------------------------
        if Complaint.objects.count() == 0 and "Customer_Complaints" in xl.sheet_names:
            df = xl.parse("Customer_Complaints")
            df.columns = [c.strip() for c in df.columns]

            objs = []
            for _, r in df.iterrows():
                d = pd.to_datetime(r.get("Date"), errors="coerce")
                objs.append(
                    Complaint(
                        complaint_id=str(r.get("Complaint ID")).strip(),
                        date=d.date() if pd.notna(d) else None,
                        region=str(r.get("Region")).strip(),
                        device_type=str(r.get("Device Type")).strip(),
                        complaint_type=str(r.get("Complaint Type")).strip(),
                        duration_hours=int(r.get("Duration of Issue (Hours)")) if pd.notna(r.get("Duration of Issue (Hours)")) else None,
                        impact_level=str(r.get("Impact Level")).strip(),
                        reported_via=str(r.get("Reported via")).strip(),
                        status=str(r.get("Status")).strip(),
                    )
                )

            Complaint.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(objs)} complaints from Customer_Complaints sheet."))
        else:
            self.stdout.write(self.style.WARNING("Complaints table already has data (or sheet missing). Skipping complaints."))

        # -------------------------
        # 3) User_Base_Usage -> DataUsage
        # -------------------------
        if DataUsage.objects.count() == 0 and "User_Base_Usage" in xl.sheet_names:
            df = xl.parse("User_Base_Usage")
            df.columns = [c.strip() for c in df.columns]

            objs = []
            for _, r in df.iterrows():
                objs.append(
                    DataUsage(
                        region=str(r.get("Region")).strip(),
                        residential_users=int(r.get("Residential Users")) if pd.notna(r.get("Residential Users")) else 0,
                        business_users=int(r.get("Business Users")) if pd.notna(r.get("Business Users")) else 0,
                        avg_data_per_user_gb=float(r.get("Avg Data/User (GB/day)")) if pd.notna(r.get("Avg Data/User (GB/day)")) else 0.0,
                        peak_usage_hours=str(r.get("Peak Usage Hours")).strip(),
                        age_group_dominant=str(r.get("Age Group Dominant")).strip(),
                        usage_pattern=str(r.get("Usage Pattern")).strip(),
                    )
                )

            DataUsage.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(objs)} usage rows from User_Base_Usage sheet."))
        else:
            self.stdout.write(self.style.WARNING("DataUsage table already has data (or sheet missing). Skipping usage."))

        # -------------------------
        # 4) Geography_Climate -> GeoClimate
        # -------------------------
        if GeoClimate.objects.count() == 0 and "Geography_Climate" in xl.sheet_names:
            df = xl.parse("Geography_Climate")
            df.columns = [c.strip() for c in df.columns]

            objs = []
            for _, r in df.iterrows():
                objs.append(
                    GeoClimate(
                        region=str(r.get("Region")).strip(),
                        terrain_type=str(r.get("Terrain Type")).strip(),
                        avg_temperature=float(r.get("Avg Temperature (°C)")) if pd.notna(r.get("Avg Temperature (°C)")) else None,
                        avg_humidity=float(r.get("Avg Humidity (%)")) if pd.notna(r.get("Avg Humidity (%)")) else None,
                        rainy_season_effect=str(r.get("Rainy Season Effect")).strip(),
                        signal_interference_level=str(r.get("Signal Interference Level")).strip(),
                    )
                )

            GeoClimate.objects.bulk_create(objs, batch_size=500, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(objs)} climate rows from Geography_Climate sheet."))
        else:
            self.stdout.write(self.style.WARNING("GeoClimate table already has data (or sheet missing). Skipping climate."))

        self.stdout.write(self.style.SUCCESS("✅ Seeding from Excel finished."))
