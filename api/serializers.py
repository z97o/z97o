from rest_framework import serializers
from dashboard.models import (
    Region, CustomerComplaint, UserBaseUsage, Infrastructure, GeographyClimate
)

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]

class ComplaintSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = CustomerComplaint
        fields = ["complaint_id","date","region","device_type","complaint_type",
                  "duration_hours","impact_level","reported_via","status"]


class UserUsageSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = UserBaseUsage
        fields = ["region", "residential_users", "business_users",
                  "avg_data_gb_per_day", "peak_usage_hours", "age_group",
                  "dominant_usage_pattern"]

class InfrastructureSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = Infrastructure
        fields = ["tower_id","region","installation_date","tower_type",
                  "technology","power_source","operational_status","max_capacity_users"]


class ClimateSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = GeographyClimate
        fields = ["region", "terrain_type", "avg_temperature_c", "avg_humidity_pct",
                  "rainy_season_effect", "signal_interference_level"]
        
        from rest_framework import serializers
from dashboard.models import SignalTower

class SignalTowerSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name", read_only=True)

    class Meta:
        model  = SignalTower
        fields = ["tower_id","name","region","lat","lng","rsrp_dbm","tech","vendor","status"]

