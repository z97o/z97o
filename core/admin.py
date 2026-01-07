# core/admin.py
from django.contrib import admin
from .models import Region, Tower, Complaint

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

@admin.register(Tower)
class TowerAdmin(admin.ModelAdmin):
    list_display = ("tower_id", "status", "region")
    list_filter = ("status", "region")
    search_fields = ("tower_id",)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("created_at", "category", "status", "priority", "region", "tower", "customer_msisdn")
    list_filter = ("status", "priority", "category", "region")
    search_fields = ("customer_msisdn", "category", "details")
