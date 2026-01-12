from pathlib import Path
import pandas as pd
import random

from django.core.management.base import BaseCommand
from django.apps import apps


BASE_DIR = Path(__file__).resolve().parents[3]
EXCEL_PATH = BASE_DIR / "data" / "NetInsight_Large_Detailed_Dataset.xlsx"
REGIONS_CSV_PATH = BASE_DIR / "data" / "regions.csv"


def model_field_names(Model):
    return {f.name for f in Model._meta.get_fields() if hasattr(f, "attname")}


def safe_str(x):
    if x is None or pd.isna(x):
        return ""
    return str(x).strip()


def to_int(x):
    try:
        if x is None or pd.isna(x):
            return None
        s = str(x).strip()
        if s == "":
            return None
        return int(float(s))
    except Exception:
        return None


def to_float(x):
    """
    Robust float converter:
    - handles None/NaN/empty
    - handles Arabic comma (،)
    - handles comma as decimal separator
    """
    try:
        if x is None or pd.isna(x):
            return None
        s = str(x).strip()
        if s == "":
            return None
        s = s.replace("،", ".").replace(",", ".")
        return float(s)
    except Exception:
        return None


def to_date(x):
    d = pd.to_datetime(x, errors="coerce")
    return d.date() if pd.notna(d) else None


def first_present(row, keys):
    """
    Return the first non-empty value from row for given keys.
    IMPORTANT: doesn't treat 0 as empty.
    """
    for k in keys:
        v = row.get(k)
        if v is None:
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        if pd.isna(v):
            continue
        return v
    return None


# City -> Big region name in regions.csv
CITY_TO_REGION_NAME = {
    "Seeb": "Muscat North",
    "Barka": "Muscat South",
    "Rustaq": "Muscat South",
    "Salalah": "Dhofar",
    "Sur": "Sharqiya",
}

# fallback centers (for cities not present in regions.csv)
REGION_CENTERS_FALLBACK = {
    "Seeb": (23.6800, 58.1800),
    "Sohar": (24.3419, 56.7290),
    "Nizwa": (22.9333, 57.5333),
    "Salalah": (17.0199, 54.0897),
    "Duqm": (19.6666, 57.7000),
    "Ibri": (23.2257, 56.5157),
    "Barka": (23.6766, 57.8861),
    "Sur": (22.5667, 59.5289),
    "Rustaq": (23.3908, 57.4244),
    "Buraimi": (24.2500, 55.7900),
    "Muscat": (23.5880, 58.3829),
}


def _norm_name(s: str) -> str:
    return safe_str(s).lower().replace("_", " ").strip()


def load_region_centers_from_csv():
    """
    regions.csv columns: code, name, latitude, longitude
    returns:
      centers_exact: { "muscat north": (lat,lng), ... }
      centers_list:  [("muscat north",(lat,lng)), ...]
    """
    if not REGIONS_CSV_PATH.exists():
        return {}, []

    df = pd.read_csv(REGIONS_CSV_PATH)
    centers_exact = {}
    centers_list = []

    for _, r in df.iterrows():
        name = _norm_name(r.get("name"))
        lat = to_float(r.get("latitude"))
        lng = to_float(r.get("longitude"))
        if name and lat is not None and lng is not None:
            centers_exact[name] = (lat, lng)
            centers_list.append((name, (lat, lng)))

    return centers_exact, centers_list


def pick_region_center(region_raw: str, centers_exact: dict, centers_list: list):
    """
    Strategy:
    0) map city -> big region
    1) exact match in CSV
    2) substring match in CSV
    3) fallback city centers
    4) default Muscat
    """
    mapped = CITY_TO_REGION_NAME.get(region_raw)
    if mapped:
        region_raw = mapped

    rnorm = _norm_name(region_raw)
    if not rnorm:
        return REGION_CENTERS_FALLBACK["Muscat"]

    if rnorm in centers_exact:
        return centers_exact[rnorm]

    for name, coords in centers_list:
        if rnorm in name or name in rnorm:
            return coords

    if region_raw in REGION_CENTERS_FALLBACK:
        return REGION_CENTERS_FALLBACK[region_raw]

    return REGION_CENTERS_FALLBACK.get(region_raw, REGION_CENTERS_FALLBACK["Muscat"])


def spread_coords(center_lat, center_lng):
    """small random spread so towers don't overlap exactly"""
    return (
        center_lat + random.uniform(-0.06, 0.06),
        center_lng + random.uniform(-0.06, 0.06),
    )


class Command(BaseCommand):
    help = "Seed database from Excel sheets safely (won't crash if some fields differ)."

    def handle(self, *args, **options):
        if not EXCEL_PATH.exists():
            self.stdout.write(self.style.ERROR(f"Excel not found: {EXCEL_PATH}"))
            return

        xl = pd.ExcelFile(EXCEL_PATH)

        # load big-region centers from CSV
        centers_exact, centers_list = load_region_centers_from_csv()
        self.stdout.write(
            self.style.SUCCESS(f"Region centers loaded from CSV: {len(centers_exact)}")
        )

        Tower = apps.get_model("dashboard", "Tower")
        Complaint = apps.get_model("dashboard", "Complaint")
        DataUsage = apps.get_model("dashboard", "DataUsage")
        GeoClimate = apps.get_model("dashboard", "GeoClimate")

        # =========================
        # 1) Infrastructure -> Tower
        # =========================
        needs_seed = (
            Tower.objects.count() == 0
            or Tower.objects.filter(latitude__isnull=True).exists()
            or Tower.objects.filter(longitude__isnull=True).exists()
            or Tower.objects.filter(latitude=0).exists()
            or Tower.objects.filter(longitude=0).exists()
        )

        if "Infrastructure" in xl.sheet_names and needs_seed:
            df = xl.parse("Infrastructure")
            df.columns = [str(c).strip() for c in df.columns]

            updated = 0
            created = 0

            for _, r in df.iterrows():
                region = safe_str(r.get("Region"))

                lat_raw = first_present(r, ["Latitude", "latitude", "LAT", "lat"])
                lng_raw = first_present(r, ["Longitude", "longitude", "LNG", "lng", "Lon", "lon", "Long"])

                lat = to_float(lat_raw)
                lng = to_float(lng_raw)

                if lat is None or lng is None:
                    base_lat, base_lng = pick_region_center(region, centers_exact, centers_list)
                    lat, lng = spread_coords(base_lat, base_lng)

                tower_id = safe_str(r.get("Tower ID"))

                defaults = {
                    "region": region,
                    "installation_date": to_date(r.get("Installation Date")),
                    "tower_type": safe_str(r.get("Tower Type")),
                    "technology": safe_str(r.get("Technology")),
                    "power_source": safe_str(r.get("Power Source")),
                    "operational_status": safe_str(r.get("Operational Status")),
                    "max_capacity_users": to_int(r.get("Max Capacity (Users)")),
                    "latitude": lat,
                    "longitude": lng,
                }

                _, was_created = Tower.objects.update_or_create(
                    tower_id=tower_id,
                    defaults=defaults
                )

                if was_created:
                    created += 1
                else:
                    updated += 1

            self.stdout.write(self.style.SUCCESS(f"Towers created: {created}, updated: {updated}"))
        else:
            self.stdout.write(self.style.WARNING("Skip towers (already seeded or sheet missing)."))

        # ==================================
        # 2) Customer_Complaints -> Complaint
        # ==================================
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

        # ============================
        # 3) User_Base_Usage -> DataUsage
        # ============================
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

        # ===============================
        # 4) Geography_Climate -> GeoClimate
        # ===============================
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
