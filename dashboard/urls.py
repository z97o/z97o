from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Home / main dashboard
    path("", views.dashboard_view, name="home"),

    # Region Insights
    path("regions/", views.region_insights_view, name="regions"),

    # Tower Map
    path("towers/", views.tower_map_view, name="towers"),

    # KPI Reports
    path("kpis/", views.kpi_reports_view, name="kpis"),

    # Complaints page
    path("complaints/", views.complaints_view, name="complaints"),

    path("kpireports/", views.kpi_reports_view, name="kpi_reports"),   # <-- ADD THIS
    path(
        "complaints/<str:complaint_id>/",
        views.complaint_detail_view,
        name="complaint_detail",
    ),

     # Auth URLs
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
     path("kpireports/", views.kpi_reports, name="kpi_reports"),
    path("kpireports/download/csv/", views.kpi_download_csv, name="kpi_download_csv"),
    path("kpireports/download/excel/", views.kpi_download_excel, name="kpi_download_excel"),

    path("alerts/mark-read/<int:alert_id>/", views.mark_alert_read, name="mark_alert_read"),
    path("alerts/simulate/", views.simulate_alert, name="simulate_alert"),
      path("alerts/latest/", views.latest_unread_alert, name="latest_alert"),
    path("tower-events/create/", views.create_tower_event, name="create_tower_event"),
    path("alerts/read/<int:alert_id>/", views.mark_alert_read, name="mark_alert_read"),


]





