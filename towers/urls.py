# towers/urls.py
from django.urls import path
from . import views

app_name = "towers"

urlpatterns = [
    path("", views.index, name="index"),
]
