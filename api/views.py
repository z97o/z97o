# api/views.py
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Sum

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.models import (
    Region,
    CustomerComplaint,
    UserBaseUsage,
    Infrastructure,
    GeographyClimate,
    NetMetric,          # <-- AI time-series
    RiskScore,          # <-- AI scores
)

from .serializers import (
    RegionSerializer,
    ComplaintSerializer,
    UserUsageSerializer,
    InfrastructureSerializer,
    ClimateSerializer,
)

from rest_framework import viewsets
from dashboard.models import SignalTower
from .serializers import SignalTowerSerializer

class SignalTowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SignalTower.objects.select_related("region").all()
    serializer_class = SignalTowerSerializer

    # Optional filters: /api/towers/?region=Muscat&tech=5G
    def get_queryset(self):
        qs = super().get_queryset()
        region = self.request.query_params.get("region")
        tech   = self.request.query_params.get("tech")
        if region and region.upper() != "ALL":
            qs = qs.filter(region__name__iexact=region)
        if tech:
            qs = qs.filter(tech__iexact=tech)
        return qs


# -----------------------------
# Basic read-only viewsets
# -----------------------------
class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all().order_by("name")
    serializer_class = RegionSerializer


class ComplaintViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomerComplaint.objects.select_related("region").all().order_by("-date")
    serializer_class = ComplaintSerializer


class UserUsageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserBaseUsage.objects.select_related("region").all()
    serializer_class = UserUsageSerializer


class InfrastructureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Infrastructure.objects.select_related("region").all()
    serializer_class = InfrastructureSerializer


class ClimateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GeographyClimate.objects.select_related("region").all()
    serializer_class = ClimateSerializer


# -----------------------------
# Summaries for charts
# -----------------------------
class ComplaintsSummary(APIView):
    def get(self, request):
        region = request.GET.get("region")
        since = request.GET.get("since")
        until = request.GET.get("until")

        qs = CustomerComplaint.objects.select_related("region")
        if region and region.upper() != "ALL":
            qs = qs.filter(region__name__iexact=region)
        if since:
            try:
                qs = qs.filter(date__gte=datetime.fromisoformat(since))
            except Exception:
                pass
        if until:
            try:
                qs = qs.filter(date__lte=datetime.fromisoformat(until))
            except Exception:
                pass

        total = qs.count()
        resolved = qs.filter(status__iexact="Resolved").count()
        resolved_rate = round((resolved / total) * 100, 1) if total else 0.0

        by_type = list(
            qs.values("complaint_type")
              .annotate(value=Count("id"))
              .order_by("-value")
        )
        for row in by_type:
            row["label"] = row.pop("complaint_type")

        dates = qs.values_list("date", flat=True).distinct().order_by("date")
        trend = []
        for d in dates:
            day = qs.filter(date=d)
            trend.append({
                "date": d.isoformat(),
                "open": day.exclude(status__iexact="Resolved").count(),
                "resolved": day.filter(status__iexact="Resolved").count(),
            })

        return Response({
            "total": total,
            "resolved_rate": resolved_rate,
            "by_type": by_type,
            "status_trend": trend,
        })


class UsersSummary(APIView):
    def get(self, request):
        region = request.GET.get("region")
        qs = UserBaseUsage.objects.select_related("region")
        if region and region.upper() != "ALL":
            qs = qs.filter(region__name__iexact=region)

        rows = [{
            "region": u.region.name,
            "residential": u.residential_users,
            "business": u.business_users,
            "avg": u.avg_data_gb_per_day,
        } for u in qs]

        return Response({"rows": rows})


class InfraSummary(APIView):
    def get(self, request):
        region = request.GET.get("region")
        qs = Infrastructure.objects.select_related("region")
        if region and region.upper() != "ALL":
            qs = qs.filter(region__name__iexact=region)

        status_counts = list(
            qs.values("operational_status")
              .annotate(value=Count("id"))
              .order_by("-value")
        )
        for row in status_counts:
            row["label"] = row.pop("operational_status")

        cap = qs.values("region__name").annotate(capacity=Sum("max_capacity_users")).order_by("-capacity")
        capacity_by_region = [{"region": r["region__name"], "capacity": r["capacity"]} for r in cap]

        return Response({
            "status_counts": status_counts,
            "capacity_by_region": capacity_by_region,
        })


class ClimateSummary(APIView):
    def get(self, request):
        region = request.GET.get("region")
        qs = GeographyClimate.objects.select_related("region")
        if region and region.upper() != "ALL":
            qs = qs.filter(region__name__iexact=region)

        rows = [{
            "region": c.region.name,
            "terrain": c.terrain_type,
            "temp": c.avg_temperature_c,
            "hum": c.avg_humidity_pct,
            "interference": c.signal_interference_level,
        } for c in qs]

        return Response({"rows": rows})


# -----------------------------
# AI health endpoints
# -----------------------------
class HealthNow(APIView):
    """
    /api/health/now?region=ALL
    Returns most recent reading + risk per region.
    """
    def get(self, request):
        region = request.GET.get("region")
        regions = Region.objects.all()
        if region and region.upper() != "ALL":
            regions = regions.filter(name__iexact=region)

        rows = []
        for r in regions:
            last = NetMetric.objects.filter(region=r).order_by("-ts").first()
            risk = RiskScore.objects.filter(region=r).order_by("-ts").first()
            if last:
                rows.append({
                    "region": r.name,
                    "ts": last.ts,
                    "download": last.download_mbps,
                    "latency": last.latency_ms,
                    "signal": last.signal_dbm,
                    "users": last.users_online,
                    "risk_prob": getattr(risk, "risk_prob", 0.0),
                    "anomaly": getattr(risk, "anomaly", False),
                })
        return Response({"rows": rows})


class HealthTrend(APIView):
    """
    /api/health/trend?region=Muscat&hours=24
    Returns recent time-series for download + latency.
    """
    def get(self, request):
        region = request.GET.get("region")
        hours = int(request.GET.get("hours", 24))
        qs = NetMetric.objects.all()
        if region and region.upper() != "ALL":
            qs = qs.filter(region__name__iexact=region)

        since = timezone.now() - timedelta(hours=hours)
        qs = qs.filter(ts__gte=since).order_by("ts")

        return Response({
            "rows": [{"ts": m.ts, "download": m.download_mbps, "latency": m.latency_ms} for m in qs]
        })
