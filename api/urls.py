from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewSet,
    ComplaintViewSet,
    UserUsageViewSet,
    InfrastructureViewSet,
    ClimateViewSet,
    SignalTowerViewSet,  # ✅ added
    ComplaintsSummary,
    UsersSummary,
    InfraSummary,
    ClimateSummary,
    HealthNow,
    HealthTrend,
)

# ----- Router for ViewSets -----
router = DefaultRouter()
router.register(r"regions", RegionViewSet, basename="regions")
router.register(r"complaints", ComplaintViewSet, basename="complaints")
router.register(r"user-usage", UserUsageViewSet, basename="user-usage")
router.register(r"infrastructure", InfrastructureViewSet, basename="infrastructure")
router.register(r"climate", ClimateViewSet, basename="climate")
router.register(r"towers", SignalTowerViewSet, basename="towers")  # ✅ ensure this line exists!

urlpatterns = [
    path("", include(router.urls)),

    # summaries
    path("summary/complaints", ComplaintsSummary.as_view()),
    path("summary/users", UsersSummary.as_view()),
    path("summary/infra", InfraSummary.as_view()),
    path("summary/climate", ClimateSummary.as_view()),

    # network health
    path("health/now", HealthNow.as_view()),
    path("health/trend", HealthTrend.as_view()),
]
