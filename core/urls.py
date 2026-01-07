# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("regions/", views.region_list, name="region-list"),
    path("towers/", views.tower_list, name="tower-list"),
    path("complaints/", views.complaint_list, name="complaint-list"),
]
