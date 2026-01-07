from django.urls import path
from . import views

app_name = "mapapp"

urlpatterns = [
    path("", views.signal_map, name="signal-map"),  # /map/
]
