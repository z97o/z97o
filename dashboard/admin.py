from django.contrib import admin
from .models import (
    RegionMetrics,
    Tower,
    Complaint,
    GeoClimate,
    FaultLog,
    TowerStatusEvent,
    DataUsage,
    Alert,
)


@admin.register(RegionMetrics)
class RegionMetricsAdmin(admin.ModelAdmin):
    list_display = (
        "region",
        "residential_users",
        "business_users",
        "avg_data_gb_per_day",
        "peak_usage_hours",
        "age_group_dominant",
        "usage_pattern",
        "timestamp",
    )
    list_filter = ("region", "peak_usage_hours", "usage_pattern")
    search_fields = ("region",)


@admin.register(Tower)
class TowerAdmin(admin.ModelAdmin):
    list_display = (
        "tower_id",
        "region",
        "installation_date",
        "tower_type",
        "technology",
        "power_source",
        "operational_status",
        "max_capacity_users",
        "latitude",
        "longitude",
    )
    list_filter = ("region", "operational_status", "technology", "tower_type")
    search_fields = ("tower_id", "region")


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "complaint_id",
        "date",
        "region",
        "device_type",
        "complaint_type",
        "duration_hours",
        "impact_level",
        "reported_via",
        "status",
    )
    list_filter = ("region", "impact_level", "reported_via", "status")
    search_fields = ("complaint_id", "region", "device_type")


@admin.register(GeoClimate)
class GeoClimateAdmin(admin.ModelAdmin):
    list_display = (
        "region",
        "terrain_type",
        "avg_temp_c",
        "avg_humidity_pct",
        "rainy_season_effect",
        "signal_interference_level",
    )
    search_fields = ("region", "terrain_type")


@admin.register(FaultLog)
class FaultLogAdmin(admin.ModelAdmin):
    list_display = (
        "tower",
        "status_before",
        "status_after",
        "note",
        "created_at",
        "resolved_at",
    )
    list_filter = ("status_before", "status_after", "created_at", "resolved_at")
    search_fields = ("tower__tower_id", "tower__region")


@admin.register(TowerStatusEvent)
class TowerStatusEventAdmin(admin.ModelAdmin):
    list_display = ("tower", "status", "at")
    list_filter = ("status", "at")
    search_fields = ("tower__tower_id", "tower__region")


@admin.register(DataUsage)
class DataUsageAdmin(admin.ModelAdmin):
    list_display = ("recorded_at", "data_gb")
    list_filter = ("recorded_at",)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("severity", "title", "region", "is_read", "created_at")
    list_filter = ("severity", "is_read", "region")
    search_fields = ("title", "message", "region")