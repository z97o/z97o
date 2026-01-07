import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime
from core.models import Region, Tower, Complaint

class Command(BaseCommand):
    help = "Import Regions, Towers, Complaints from CSV files"

    def add_arguments(self, parser):
        parser.add_argument("--regions", default="data/regions.csv", help="Path to regions.csv")
        parser.add_argument("--towers", default="data/towers.csv", help="Path to towers.csv")
        parser.add_argument("--complaints", default="data/complaints.csv", help="Path to complaints.csv")
        parser.add_argument("--update", action="store_true", help="Update existing rows if keys match")

    def handle(self, *args, **opts):
        regions_path = Path(opts["regions"])
        towers_path = Path(opts["towers"])
        complaints_path = Path(opts["complaints"])
        update = opts["update"]

        if not regions_path.exists():
            raise CommandError(f"Regions file not found: {regions_path}")

        created_r = self.import_regions(regions_path, update)
        self.stdout.write(self.style.SUCCESS(f"Regions imported/updated: {created_r}"))

        if towers_path.exists():
            created_t = self.import_towers(towers_path, update)
            self.stdout.write(self.style.SUCCESS(f"Towers imported/updated: {created_t}"))
        else:
            self.stdout.write(self.style.WARNING(f"Towers file not found: {towers_path} (skipped)"))

        if complaints_path.exists():
            created_c = self.import_complaints(complaints_path, update)
            self.stdout.write(self.style.SUCCESS(f"Complaints imported/updated: {created_c}"))
        else:
            self.stdout.write(self.style.WARNING(f"Complaints file not found: {complaints_path} (skipped)"))

        self.stdout.write(self.style.SUCCESS("Done."))

    # ---------- Helpers ----------
    def safe_float(self, v):
        if v is None: return None
        v = str(v).strip()
        if not v: return None
        try:
            return float(v)
        except ValueError:
            return None

    def import_regions(self, path: Path, update: bool):
        count = 0
        with path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = (row.get("code") or "").strip()
                name = (row.get("name") or "").strip()
                if not code or not name:
                    continue
                lat = self.safe_float(row.get("latitude"))
                lng = self.safe_float(row.get("longitude"))

                obj, created = Region.objects.get_or_create(code=code, defaults={"name": name, "latitude": lat, "longitude": lng})
                if not created and update:
                    obj.name = name or obj.name
                    if lat is not None: obj.latitude = lat
                    if lng is not None: obj.longitude = lng
                    obj.save()
                    created = True  # count as affected
                if created:
                    count += 1
        return count

    def import_towers(self, path: Path, update: bool):
        count = 0
        with path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("name") or "").strip()
                region_code = (row.get("region_code") or "").strip()
                if not name or not region_code:
                    continue

                lat = self.safe_float(row.get("latitude"))
                lng = self.safe_float(row.get("longitude"))
                status = (row.get("status") or "active").strip().lower()

                try:
                    region = Region.objects.get(code=region_code)
                except Region.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Tower '{name}': Region '{region_code}' not found. Skipped."))
                    continue

                obj, created = Tower.objects.get_or_create(
                    name=name, region=region,
                    defaults={"latitude": lat, "longitude": lng, "status": status}
                )
                if not created and update:
                    if lat is not None: obj.latitude = lat
                    if lng is not None: obj.longitude = lng
                    if status: obj.status = status
                    obj.save()
                    created = True
                if created:
                    count += 1
        return count

    def import_complaints(self, path: Path, update: bool):
        count = 0
        with path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = (row.get("title") or "").strip()
                region_code = (row.get("region_code") or "").strip()
                if not title or not region_code:
                    continue

                tower_name = (row.get("tower_name") or "").strip()
                category = (row.get("category") or "General").strip()
                priority = (row.get("priority") or "low").strip().lower()
                status = (row.get("status") or "open").strip().lower()
                created_at = (row.get("created_at") or "").strip()

                try:
                    region = Region.objects.get(code=region_code)
                except Region.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Complaint '{title}': Region '{region_code}' not found. Skipped."))
                    continue

                tower = None
                if tower_name:
                    tower = Tower.objects.filter(name=tower_name, region=region).first()

                # مفتاح تطابق بسيط لمنع التكرار
                match_qs = Complaint.objects.filter(title=title, region=region)
                if tower:
                    match_qs = match_qs.filter(tower=tower)

                if match_qs.exists():
                    if update:
                        obj = match_qs.first()
                        obj.category = category or obj.category
                        obj.priority = priority or obj.priority
                        obj.status = status or obj.status
                        if created_at:
                            dt = parse_datetime(created_at) or obj.created_at
                            # created_at auto_add; لا نعدّله لو فشل التحويل
                        obj.save()
                        count += 1
                    # لو مافي update، نتجاهل
                    continue

                obj = Complaint(
                    title=title, region=region, tower=tower,
                    category=category, priority=priority, status=status,
                )
                # created_at يُملأ تلقائيًا؛ إذا عندنا قيمة صحيحة ممكن نستخدمها بعد الحفظ
                obj.save()
                # محاولة تعيين created_at إن كان مُدخلًا بصيغة صحيحة
                if created_at:
                    dt = parse_datetime(created_at)
                    if dt:
                        Complaint.objects.filter(pk=obj.pk).update(created_at=dt)
                count += 1
        return count
