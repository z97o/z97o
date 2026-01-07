from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings


class RegionMetrics(models.Model):
    region = models.CharField(max_length=100, null=True, blank=True)
    residential_users = models.IntegerField(default=0, null=True, blank=True)
    business_users = models.IntegerField(default=0, null=True, blank=True)
    avg_data_gb_per_day = models.FloatField(default=0.0, null=True, blank=True)
    peak_usage_hours = models.CharField(max_length=50, null=True, blank=True)
    age_group_dominant = models.CharField(max_length=50, null=True, blank=True)
    usage_pattern = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.region or "Unknown"



class Tower(models.Model):
    tower_id = models.CharField(max_length=50, unique=True)
    region = models.CharField(max_length=100)
    installation_date = models.DateField(null=True, blank=True)
    tower_type = models.CharField(max_length=100, null=True, blank=True)
    technology = models.CharField(max_length=100, null=True, blank=True)
    power_source = models.CharField(max_length=100, null=True, blank=True)
    operational_status = models.CharField(max_length=100, null=True, blank=True)
    max_capacity_users = models.IntegerField(null=True, blank=True)
    # coords (nullable so migrations won’t block)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.tower_id} - {self.region}"


class Complaint(models.Model):
    complaint_id = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    region = models.CharField(max_length=100)

    # الحقول الخاصة بنوع الجهاز والشكوى
    device_type = models.CharField(max_length=100, null=True, blank=True)
    complaint_type = models.CharField(
        max_length=50,
        default="Other",
        null=True,
        blank=True,
    )

    # مدة المشكلة
    duration_hours = models.FloatField(default=0)

    # مستوى التأثير + طريقة الإبلاغ
    impact_level = models.CharField(max_length=50, null=True, blank=True)
    reported_via = models.CharField(max_length=50, null=True, blank=True)

    # حالة الشكوى (مفتوحة، مغلقة، قيد المتابعة...)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.region}"



class FaultLog(models.Model):
    tower = models.ForeignKey("Tower", on_delete=models.CASCADE, related_name="fault_logs")
    status_before = models.CharField(max_length=100, blank=True, default="")
    status_after = models.CharField(max_length=100, blank=True, default="")
    note = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        ident = getattr(self.tower, "tower_id", None) or f"Tower#{self.tower_id}"
        return f"FaultLog({ident} {self.status_before}→{self.status_after} @ {self.resolved_at:%Y-%m-%d %H:%M})"
    

class TowerStatusEvent(models.Model):
    tower = models.ForeignKey("Tower", on_delete=models.CASCADE, related_name="status_events")
    status = models.CharField(max_length=100)
    at = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        # Fix: reference the related tower correctly
        return f"{self.tower.tower_id} {self.status} @ {self.at:%Y-%m-%d %H:%M}"


@receiver(pre_save, sender=Tower)
def _log_status_change(sender, instance: "Tower", **kwargs):
    # Only log after the object exists (updates)
    if not instance.pk:
        return
    try:
        prev = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    if (prev.operational_status or "").lower() != (instance.operational_status or "").lower():
        TowerStatusEvent.objects.create(tower=instance, status=instance.operational_status)


class DataUsage(models.Model):
    recorded_at = models.DateTimeField()
    data_gb = models.FloatField()

    def __str__(self):
        return f"{self.recorded_at:%Y-%m-%d} – {self.data_gb} GB"

class GeoClimate(models.Model):
    region = models.CharField(max_length=100, unique=True)
    terrain_type = models.CharField(max_length=100, null=True, blank=True)
    avg_temp_c = models.FloatField(null=True, blank=True)
    avg_humidity_pct = models.FloatField(null=True, blank=True)
    rainy_season_effect = models.CharField(max_length=200, null=True, blank=True)
    signal_interference_level = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.region
    
class KPIRecord(models.Model):
    region = models.CharField(max_length=100)
    kpi_date = models.DateField()

    download_mbps = models.FloatField(null=True, blank=True)
    upload_mbps = models.FloatField(null=True, blank=True)
    latency_ms = models.FloatField(null=True, blank=True)
    uptime_percent = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.region} - {self.kpi_date}"
    

class Alert(models.Model):
    SEVERITY_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="INFO")

    region = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.severity}] {self.title}"