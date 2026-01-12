from django.shortcuts import render
from django.conf import settings
from pathlib import Path
from django.db import transaction
import pandas as pd
import json
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
import csv
import io
from datetime import datetime
from .models import Complaint
from .forms import KPIImportForm
from django.http import HttpResponse
from openpyxl import Workbook
from dashboard.models import KPIRecord
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import random


# Path to your NetInsight dataset
DATA_FILE = Path(settings.BASE_DIR) / "data" / "NetInsight_Large_Detailed_Dataset.xlsx"


# ─────────────────────────────
# ALERT BUILDER
# ─────────────────────────────
def build_alerts():
    """
    Alerts from DB (MySQL) not from Excel.
    Rules:
      - If there is any DOWN tower => Network Not Stable (Critical)
      - Else if any Maintenance => Network Not Stable (Warning)
      - Else => Network Stable (OK)

    Also: show latest unread alert from Alert table (if exists)
    """

    alerts = []

    # 0) لو عندك نظام alerts من TowerStatusEvent → خلّه يولد alerts
    # (اختياري) توليد Alerts من events آخر ساعة:
    try:
        generate_alerts_from_tower_events(minutes=60)
    except Exception as e:
        print("generate_alerts_from_tower_events error:", e)

    # 1) اقرأ حالات الأبراج من DB
    down_count = Tower.objects.filter(operational_status__iexact="Down").count()
    maint_count = Tower.objects.filter(operational_status__iexact="Maintenance").count()

    # 2) لو في Alerts غير مقروءة (Unread) اعرض أحدث واحد
    latest_unread = Alert.objects.filter(is_read=False).order_by("-created_at").first()
    if latest_unread:
        alerts.append({
            "category": "Tower",
            "severity": getattr(latest_unread, "level", "critical"),
            "title": latest_unread.title,
            "message": latest_unread.message,
            "icon": "🚨" if getattr(latest_unread, "level", "") == "critical" else "⚠️",
        })

    # 3) حالة الشبكة (Stable / Not Stable)
    if down_count > 0:
        alerts.append({
            "category": "System",
            "severity": "critical",
            "title": "Network Not Stable",
            "message": f"{down_count} tower(s) are DOWN. Immediate action required.",
            "icon": "🚨",
        })
    elif maint_count > 0:
        alerts.append({
            "category": "System",
            "severity": "medium",
            "title": "Network Not Stable",
            "message": f"{maint_count} tower(s) are under Maintenance.",
            "icon": "⚠️",
        })
    else:
        alerts.append({
            "category": "System",
            "severity": "ok",
            "title": "Network Stable",
            "message": "No major issues detected across regions.",
            "icon": "✅",
        })

    return alerts





# ─────────────────────────────
# HOME / DASHBOARD VIEW
# ─────────────────────────────
@login_required
def dashboard_view(request):
    """
    Main landing dashboard.
    Shows KPIs from Excel + Tower Map from database + Alerts + Charts.
    """

    # ────────── LOAD DATA FROM EXCEL ──────────
    user_df = pd.read_excel(DATA_FILE, sheet_name="User_Base_Usage")
    comp_df = pd.read_excel(DATA_FILE, sheet_name="Customer_Complaints")
    infra_df = pd.read_excel(DATA_FILE, sheet_name="Infrastructure")

    # Total users
    user_df["Total Users"] = user_df["Residential Users"] + user_df["Business Users"]
    total_residential = int(user_df["Residential Users"].sum())
    total_business = int(user_df["Business Users"].sum())
    total_users = int(user_df["Total Users"].sum())

    # Complaints count
    total_complaints = int(comp_df["Complaint ID"].count())

    # Towers summary from Excel
    # ✅ Towers summary from DB (MySQL)
    total_towers = Tower.objects.count()
    active_towers = Tower.objects.filter(operational_status__iexact="Active").count()
    maintenance_towers = Tower.objects.filter(operational_status__iexact="Maintenance").count()
    down_towers = Tower.objects.filter(operational_status__iexact="Down").count()


    # Top region by users
    top_region_users = (
        user_df.sort_values("Total Users", ascending=False)
        .iloc[0]["Region"]
    )

    # Top region by complaints
    complaints_by_region = (
        comp_df.groupby("Region")["Complaint ID"]
        .count()
        .reset_index(name="Complaint Count")
    )
    if not complaints_by_region.empty:
        top_region_complaints = (
            complaints_by_region.sort_values("Complaint Count", ascending=False)
            .iloc[0]["Region"]
        )
    else:
        top_region_complaints = "N/A"

    # ────────── TOWER DATA FOR MAP (FROM DATABASE) ──────────
    towers_qs = Tower.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)

    tower_points = []
    for t in towers_qs:
        tower_points.append(
            {
                "tower_id": t.tower_id,
                "region": t.region,
                "lat": t.latitude,
                "lng": t.longitude,
                "status": t.operational_status or "Unknown",
                "technology": t.technology or "-",
                "tower_type": t.tower_type or "-",
                "max_capacity_users": t.max_capacity_users or 0,
            }
        )

    # ────────── ALERTS (from Excel) ──────────
    alerts = build_alerts()

    # ────────── CHART DATA ──────────
    # 1) Users per region (bar chart)
    region_usage = (
        user_df.groupby("Region")["Total Users"]
        .sum()
        .reset_index()
        .sort_values("Total Users", ascending=False)
    )
    chart_users_region_labels = region_usage["Region"].tolist()
    chart_users_region_values = region_usage["Total Users"].tolist()

    # 2) Complaints per region (bar chart)
    complaints_region_sorted = complaints_by_region.sort_values(
        "Complaint Count", ascending=False
    )
    chart_complaints_region_labels = complaints_region_sorted["Region"].tolist()
    chart_complaints_region_values = complaints_region_sorted["Complaint Count"].tolist()

    # 3) Tower status (doughnut chart)
    chart_tower_status_labels = ["Active", "Maintenance", "Down"]
    chart_tower_status_values = [active_towers, maintenance_towers, down_towers]

    # ────────── CONTEXT TO TEMPLATE ──────────
    context = {
        "total_residential": total_residential,
        "total_business": total_business,
        "total_users": total_users,
        "total_complaints": total_complaints,
        "total_towers": total_towers,
        "active_towers": active_towers,
        "maintenance_towers": maintenance_towers,
        "down_towers": down_towers,
        "top_region_users": top_region_users,
        "top_region_complaints": top_region_complaints,

        # MAP DATA
        "tower_points": tower_points,
        "now": timezone.now(),

        # ALERTS
        "alerts": alerts,

        # CHART DATA (JSON for Chart.js)
        "chart_users_region_labels": json.dumps(chart_users_region_labels),
        "chart_users_region_values": json.dumps(chart_users_region_values),
        "chart_complaints_region_labels": json.dumps(chart_complaints_region_labels),
        "chart_complaints_region_values": json.dumps(chart_complaints_region_values),
        "chart_tower_status_labels": json.dumps(chart_tower_status_labels),
        "chart_tower_status_values": json.dumps(chart_tower_status_values),
    }

    return render(request, "dashboard/home.html", context)


# ─────────────────────────────
# REGION INSIGHTS VIEW
# ─────────────────────────────
def region_insights_view(request):
    """
    Region KPI page:
    - Total users per region
    - Average data per user
    - Complaint counts per region
    """
    # Read sheets
    user_df = pd.read_excel(DATA_FILE, sheet_name="User_Base_Usage")
    comp_df = pd.read_excel(DATA_FILE, sheet_name="Customer_Complaints")

    # Complaints per region
    complaints_by_region = (
        comp_df.groupby("Region")["Complaint ID"]
        .count()
        .reset_index(name="Complaint Count")
    )

    # Merge usage + complaints
    summary = user_df.merge(complaints_by_region, on="Region", how="left").fillna(0)

    # Add total users
    summary["Total Users"] = summary["Residential Users"] + summary["Business Users"]

    # Rename columns to safe keys for templates
    summary_for_template = summary.rename(
        columns={
            "Region": "region",
            "Residential Users": "res_users",
            "Business Users": "bus_users",
            "Total Users": "total_users",
            "Avg Data/User (GB/day)": "avg_data",
            "Complaint Count": "complaints",
        }
    )

    # Lists for charts
    regions = summary_for_template["region"].tolist()
    total_users = summary_for_template["total_users"].tolist()
    avg_data = summary_for_template["avg_data"].tolist()
    complaints = summary_for_template["complaints"].tolist()

    # Table rows
    rows = summary_for_template.to_dict("records")

    context = {
        "regions": regions,
        "total_users": total_users,
        "avg_data": avg_data,
        "complaints": complaints,
        "rows": rows,
    }
    return render(request, "dashboard/region_insights.html", context)


# ─────────────────────────────
# TOWER MAP VIEW
# ─────────────────────────────
def _safe_float(x):
    """
    يحول أي قيمة لرقم float بأمان:
    - يتعامل مع None / فراغ
    - يتعامل مع "23,588" أو "23.588" أو "23،588"
    """
    if x is None:
        return None
    s = str(x).strip()
    if s == "":
        return None
    s = s.replace("،", ".").replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None



@login_required
def tower_map_view(request):
    towers_all = Tower.objects.all()

    towers_qs = (
        towers_all
        .exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .exclude(latitude="")
        .exclude(longitude="")
        .exclude(latitude=0)
        .exclude(longitude=0)
    )

    towers = []
    for t in towers_qs:
        try:
            lat = float(t.latitude)
            lon = float(t.longitude)
        except Exception:
            continue

        towers.append({
            "id": t.id,
            "tower_id": t.tower_id,
            "region": t.region,
            "lat": lat,
            "lon": lon,
            "technology": t.technology or "-",
            "power_source": t.power_source or "-",
            "status": t.operational_status or "Down",
            "capacity": int(t.capacity or 0),
        })

    context = {
        "towers_json": towers,
        "total_towers": towers_all.count(),
        "active_count": towers_qs.filter(operational_status__iexact="Active").count(),
        "maintenance_count": towers_qs.filter(operational_status__iexact="Maintenance").count(),
        "down_count": towers_qs.filter(operational_status__iexact="Down").count(),
        "mapped_towers": len(towers),  # 👈 هذا اللي نعرضه في الصفحة
    }

    return render(request, "towers/tower_map.html", context)


# ─────────────────────────────
# KPI REPORTS VIEW
# ─────────────────────────────
def kpi_reports_view(request):
    """
    KPI Reports dashboard:
    - Overall complaint KPIs
    - Complaints trend over time
    - Complaints per region
    - Complaint rate per 10k users
    - Complaint type distribution
    """
    # Load data from the correct sheets
    user_df = pd.read_excel(DATA_FILE, sheet_name="User_Base_Usage")
    comp_df = pd.read_excel(DATA_FILE, sheet_name="Customer_Complaints")

    # Make sure Date is datetime
    comp_df["Date"] = pd.to_datetime(comp_df["Date"])

    # ───── Top Summary KPIs ─────
    total_complaints = int(len(comp_df))
    open_complaints = int((comp_df["Status"] == "Open").sum())
    resolved_complaints = int((comp_df["Status"] == "Resolved").sum())
    avg_duration = float(comp_df["Duration of Issue (Hours)"].mean() or 0.0)

    # ───── Complaints trend over time (by day) ─────
    daily = (
        comp_df.groupby("Date")["Complaint ID"]
        .count()
        .reset_index(name="Complaint Count")
        .sort_values("Date")
    )
    dates = [d.strftime("%Y-%m-%d") for d in daily["Date"]]
    daily_counts = daily["Complaint Count"].tolist()

    # ───── Complaints by region ─────
    by_region = (
        comp_df.groupby("Region")["Complaint ID"]
        .count()
        .reset_index(name="Complaint Count")
        .sort_values("Complaint Count", ascending=False)
    )
    regions = by_region["Region"].tolist()
    region_counts = by_region["Complaint Count"].tolist()

    # ───── Complaint rate per 10k users ─────
    user_df["Total Users"] = user_df["Residential Users"] + user_df["Business Users"]

    summary = user_df.merge(by_region, on="Region", how="left").fillna(0)
    summary["Complaint Rate per 10k"] = summary.apply(
        lambda r: (r["Complaint Count"] / r["Total Users"] * 10000)
        if r["Total Users"] > 0
        else 0,
        axis=1,
    )

    rate_df = summary.sort_values("Complaint Rate per 10k", ascending=False)
    rate_regions = rate_df["Region"].tolist()
    rates = [round(x, 2) for x in rate_df["Complaint Rate per 10k"].tolist()]

    # ───── Complaint type distribution (top 6) ─────
    type_df = (
        comp_df.groupby("Complaint Type")["Complaint ID"]
        .count()
        .reset_index(name="Complaint Count")
        .sort_values("Complaint Count", ascending=False)
        .head(6)
    )
    complaint_types = type_df["Complaint Type"].tolist()
    type_counts = type_df["Complaint Count"].tolist()

    context = {
        # Summary cards
        "total_complaints": total_complaints,
        "open_complaints": open_complaints,
        "resolved_complaints": resolved_complaints,
        "avg_duration": round(avg_duration, 1),

        # Trend chart
        "dates": dates,
        "daily_counts": daily_counts,

        # Complaints per region
        "regions": regions,
        "region_counts": region_counts,

        # Complaint rate per 10k
        "rate_regions": rate_regions,
        "rates": rates,

        # Complaint type distribution
        "complaint_types": complaint_types,
        "type_counts": type_counts,
    }
    return render(request, "dashboard/kpi_reports.html", context)


# ─────────────────────────────
# COMPLAINTS VIEW
# ─────────────────────────────
def complaints_view(request):
    # Load complaints sheet
    comp_df = pd.read_excel(DATA_FILE, sheet_name="Customer_Complaints")

    # Ensure Date is datetime
    comp_df["Date"] = pd.to_datetime(comp_df["Date"])

    # ---- Filter options (for dropdowns) ----
    regions_list = sorted(comp_df["Region"].dropna().unique().tolist())
    status_list = sorted(comp_df["Status"].dropna().unique().tolist())
    type_list = sorted(comp_df["Complaint Type"].dropna().unique().tolist())

    # ---- Read filter values from URL (?region=...&status=...&type=...&q=...) ----
    region_filter = request.GET.get("region", "all")
    status_filter = request.GET.get("status", "all")
    type_filter = request.GET.get("ctype", "all")
    search_q = request.GET.get("q", "").strip()

    df = comp_df.copy()

    if region_filter != "all":
        df = df[df["Region"] == region_filter]

    if status_filter != "all":
        df = df[df["Status"] == status_filter]

    if type_filter != "all":
        df = df[df["Complaint Type"] == type_filter]

    if search_q:
        # Search in Complaint ID, Region, Complaint Type
        mask = (
            df["Complaint ID"].astype(str).str.contains(search_q, case=False, na=False)
            | df["Region"].str.contains(search_q, case=False, na=False)
            | df["Complaint Type"].str.contains(search_q, case=False, na=False)
        )
        df = df[mask]

    # Sort latest first
    df = df.sort_values("Date", ascending=False)

    # ---- Summary KPIs (after filters) ----
    total_complaints = int(len(df))
    open_complaints = int((df["Status"] == "Open").sum())
    resolved_complaints = int((df["Status"] == "Resolved").sum())
    avg_duration = float(df["Duration of Issue (Hours)"].mean() or 0.0)

    # ---- Chart 1: Complaints by Type (top 5) ----
    type_counts = (
        df.groupby("Complaint Type")["Complaint ID"]
        .count()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
        .head(5)
    )
    chart_types = type_counts["Complaint Type"].tolist()
    chart_type_counts = type_counts["Count"].tolist()

    # ---- Chart 2: Avg Duration by Region (top 5) ----
    dur_region = (
        df.groupby("Region")["Duration of Issue (Hours)"]
        .mean()
        .reset_index(name="AvgDuration")
        .sort_values("AvgDuration", ascending=False)
        .head(5)
    )
    chart_regions = dur_region["Region"].tolist()
    chart_regions_avg = [round(x, 1) for x in dur_region["AvgDuration"].tolist()]

    # ---- Table data ----
    table_records = df[
        [
            "Complaint ID",
            "Date",
            "Region",
            "Complaint Type",
            "Status",
            "Duration of Issue (Hours)",
        ]
    ].to_dict(orient="records")

    context = {
        # table
        "complaints": table_records,

        # summary
        "total_complaints": total_complaints,
        "open_complaints": open_complaints,
        "resolved_complaints": resolved_complaints,
        "avg_duration": round(avg_duration, 1),

        # filters (options)
        "regions_list": regions_list,
        "status_list": status_list,
        "type_list": type_list,

        # current filter values
        "region_filter": region_filter,
        "status_filter": status_filter,
        "type_filter": type_filter,
        "search_q": search_q,

        # chart data
        "chart_types": chart_types,
        "chart_type_counts": chart_type_counts,
        "chart_regions": chart_regions,
        "chart_regions_avg": chart_regions_avg,
    }

    return render(request, "dashboard/complaints.html", context)


# ─────────────────────────────
# SINGLE COMPLAINT DETAIL
# ─────────────────────────────
def complaint_detail_view(request, complaint_id):
    """Show full details for a single complaint."""
    comp_df = pd.read_excel(DATA_FILE, sheet_name="Customer_Complaints")
    comp_df["Date"] = pd.to_datetime(comp_df["Date"])

    row = comp_df.loc[comp_df["Complaint ID"] == complaint_id]

    if row.empty:
        raise Http404("Complaint not found")

    record = row.iloc[0].to_dict()

    context = {
        "complaint": record,
    }
    return render(request, "dashboard/complaint_detail.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")   # ✔ FIXED

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard:home")   # ✔ FIXED
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)

    return render(request, "dashboard/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")   # ← هنا التغيير

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login user after register (optional)
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("dashboard:home")   # ← وهنا أيضًا
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, "dashboard/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("dashboard:login")

def kpi_reports(request):
    qs, region, date_from, date_to = _filtered_kpi_queryset(request)

    context = {
        "records": qs[:300],              # بيانات الجدول
        "records_count": qs.count(),      # عدد النتائج
        "region": region,
        "date_from": date_from,
        "date_to": date_to,
    }
    return render(request, "dashboard/kpi_reports.html", context)


def kpi_import(request):
    if request.method != "POST":
        return redirect("kpi_reports")

    form = KPIImportForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Please upload a valid CSV file.")
        return redirect("kpi_reports")

    uploaded_file = request.FILES["file"]

    try:
        data = uploaded_file.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(data))

        created_count = 0
        updated_count = 0

        for row in reader:
            region = (row.get("region") or "").strip()
            kpi_date = (row.get("kpi_date") or "").strip()

            if not region or not kpi_date:
                continue

            # date format: YYYY-MM-DD (recommended)
            try:
                date_obj = datetime.strptime(kpi_date, "%Y-%m-%d").date()
            except ValueError:
                # fallback: DD/MM/YYYY
                date_obj = datetime.strptime(kpi_date, "%d/%m/%Y").date()

            def to_float(x):
                x = (x or "").strip()
                return float(x) if x else None

            defaults = {
                "download_mbps": to_float(row.get("download_mbps")),
                "upload_mbps": to_float(row.get("upload_mbps")),
                "latency_ms": to_float(row.get("latency_ms")),
                "uptime_percent": to_float(row.get("uptime_percent")),
            }

            obj, created = KPIRecord.objects.update_or_create(
                region=region,
                kpi_date=date_obj,
                defaults=defaults
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        messages.success(request, f"Import done ✅ Created: {created_count}, Updated: {updated_count}")
        return redirect("kpi_reports")

    except Exception as e:
        messages.error(request, f"Import failed: {e}")
        return redirect("kpi_reports")


def kpi_download_csv(request):
    qs, _, _, _ = _filtered_kpi_queryset(request)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="kpi_records.csv"'

    writer = csv.writer(response)
    writer.writerow(["region", "kpi_date", "download_mbps", "upload_mbps", "latency_ms", "uptime_percent"])

    for r in qs:
        writer.writerow([
            r.region,
            r.kpi_date,
            r.download_mbps,
            r.upload_mbps,
            r.latency_ms,
            r.uptime_percent,
        ])

    return response




def kpi_download_excel(request):
    qs, _, _, _ = _filtered_kpi_queryset(request)

    wb = Workbook()
    ws = wb.active
    ws.title = "KPI Records"

    ws.append(["region", "kpi_date", "download_mbps", "upload_mbps", "latency_ms", "uptime_percent"])

    for r in qs:
        ws.append([
            r.region,
            str(r.kpi_date),
            r.download_mbps,
            r.upload_mbps,
            r.latency_ms,
            r.uptime_percent,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="kpi_records.xlsx"'
    wb.save(response)
    return response

def _kpi_queryset(request):
    """
    نفس فلترة صفحة KPI Reports.
    عدلي أسماء الفلاتر حسب الموجود عندك في الصفحة.
    """
    qs = Complaint.objects.all()

    region = request.GET.get("region")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    status = request.GET.get("status")  # optional

    if region:
        qs = qs.filter(region__icontains=region)

    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)

    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)

    if status:
        qs = qs.filter(status__iexact=status)

    return qs

def _kpi_context(request):
    """
    رجّعي هنا نفس القيم اللي ترسليها لصفحة kpi_reports
    (استخدمي نفس الكود الموجود داخل view kpi_reports عندك)
    """
    # IMPORTANT: هنا لازم تنقلي نفس حساباتك من kpi_reports
    # مثال (بدّليه بكودك الحقيقي):
    context = {
        "total_complaints": 0,
        "open_complaints": 0,
        "resolved_complaints": 0,
        "avg_duration": 0,

        "dates": [],
        "daily_counts": [],

        "regions": [],
        "region_counts": [],

        "rate_regions": [],
        "rates": [],

        "complaint_types": [],
        "type_counts": [],
    }
    return context
def _filtered_kpi_queryset(request):
    region = request.GET.get("region", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    qs = KPIRecord.objects.all().order_by("-kpi_date")

    if region:
        qs = qs.filter(region__icontains=region)

    if date_from:
        qs = qs.filter(kpi_date__gte=date_from)

    if date_to:
        qs = qs.filter(kpi_date__lte=date_to)

    return qs, region, date_from, date_to


def kpi_reports_view(request):
    qs, region, date_from, date_to = _filtered_kpi_queryset(request)

    context = {
        "records": qs[:300],
        "records_count": qs.count(),
        "region": region,
        "date_from": date_from,
        "date_to": date_to,
    }
    return render(request, "dashboard/kpi_reports.html", context)

def latest_unread_alert(request):
    a = Alert.objects.filter(is_read=False).order_by("-created_at").first()
    if not a:
        return JsonResponse({"has_alert": False})

    return JsonResponse({
        "has_alert": True,
        "id": a.id,
        "title": a.title,
        "message": a.message,
        "level": getattr(a, "level", "info"),
        "created_at": a.created_at.strftime("%Y-%m-%d %H:%M"),
    })


@require_POST
def mark_alert_read(request, alert_id):
    Alert.objects.filter(id=alert_id).update(is_read=True)
    return JsonResponse({"ok": True})

@login_required
def simulate_alert(request):
    a = Alert.objects.create(
        title="Simulated Issue",
        message="Tower down detected in Nizwa (test).",
        level="critical",   # لو عندك field
        is_read=False,
        created_at=timezone.now(),
    )
    return JsonResponse({"ok": True, "id": a.id})

def generate_alerts_from_tower_events(minutes=60):
    since = timezone.now() - timezone.timedelta(minutes=minutes)

    latest = (TowerStatusEvent.objects
              .filter(at__gte=since, status__iexact="down")
              .select_related("tower")
              .order_by("-at")
              .first())

    if not latest:
        return None

    t = latest.tower
    title = f"Tower DOWN: {t.tower_id} ({t.region})"
    message = f"Tower {t.tower_id} in {t.region} is DOWN at {latest.at:%Y-%m-%d %H:%M}."

    alert, created = Alert.objects.get_or_create(
        title=title,
        message=message,
        is_read=False,
        defaults={"level": "critical"},
    )

    if not created and alert.is_read:
        alert.is_read = False
        alert.save(update_fields=["is_read"])

    return alert

@require_POST
@login_required
def create_tower_event(request):
    tower_pk = request.POST.get("tower_id")  # هذا هو PK للـTower (id)
    status = (request.POST.get("status") or "down").lower()

    tower = get_object_or_404(Tower, id=tower_pk)

    # 1) Create tower status event
    TowerStatusEvent.objects.create(
        tower=tower,
        status=status,
        at=timezone.now()
    )

    # 2) Create / Update alert مباشرة (ممتاز للمقيم)
    if status == "down":
        title = f"Tower DOWN: {tower.tower_id} ({tower.region})"
        message = f"Tower {tower.tower_id} in {tower.region} is DOWN at {timezone.now():%Y-%m-%d %H:%M}."

        alert, created = Alert.objects.get_or_create(
            title=title,
            message=message,
            defaults={"is_read": False, "level": "critical"} if hasattr(Alert, "level") else {"is_read": False},
        )
        if not created and getattr(alert, "is_read", False):
            alert.is_read = False
            alert.save(update_fields=["is_read"])

    elif status == "up":
        # (اختياري) تنشئي Alert لعودة الخدمة
        title = f"Tower UP: {tower.tower_id} ({tower.region})"
        message = f"Tower {tower.tower_id} in {tower.region} is back UP at {timezone.now():%Y-%m-%d %H:%M}."

        if hasattr(Alert, "level"):
            Alert.objects.create(title=title, message=message, level="info", is_read=False, created_at=timezone.now())
        else:
            Alert.objects.create(title=title, message=message, is_read=False, created_at=timezone.now())

    return JsonResponse({"ok": True})


def seed_towers_from_excel():
    """
    Reads Infrastructure sheet and inserts Towers into DB.
    Adds pseudo lat/lon around region center (jitter) so towers show separately on map.
    """
    infra = pd.read_excel(DATA_FILE, sheet_name="Infrastructure")

    # Center coordinates per region (تقريبية)
    region_coords = {
        "Seeb":    (23.6703, 58.1891),
        "Sohar":   (24.3470, 56.7075),
        "Nizwa":   (22.9333, 57.5333),
        "Salalah": (17.0190, 54.0897),
        "Duqm":    (19.6667, 57.7000),
        "Ibri":    (23.2257, 56.5151),
        "Barka":   (23.7076, 57.8890),
        "Sur":     (22.5667, 59.5289),
        "Rustaq":  (23.3908, 57.4244),
        "Buraimi": (24.2500, 55.7833),
    }

    # مقدار تحريك بسيط حول مركز المنطقة (تقريباً 3-8 كم)
    JITTER = 0.03

    created = 0
    updated = 0

    with transaction.atomic():
        for _, row in infra.iterrows():
            region = str(row.get("Region", "")).strip()
            tower_id = str(row.get("Tower ID", "")).strip()
            if not region or not tower_id:
                continue

            base = region_coords.get(region)
            if not base:
                # إذا في Region غير موجود عندنا، عطه مركز عمان تقريباً
                base = (21.5, 57.0)

            lat0, lon0 = base
            lat = lat0 + random.uniform(-JITTER, JITTER)
            lon = lon0 + random.uniform(-JITTER, JITTER)

            defaults = {
                "region": region,
                "installation_date": row.get("Installation Date") if "Installation Date" in row else None,
                "tower_type": str(row.get("Tower Type", "")).strip() or None,
                "technology": str(row.get("Technology", "")).strip() or None,
                "power_source": str(row.get("Power Source", "")).strip() or None,
                "operational_status": str(row.get("Operational Status", "")).strip() or None,
                "max_capacity_users": int(row.get("Max Capacity (Users)", 0) or 0),
                "latitude": lat,
                "longitude": lon,
            }

            obj, was_created = Tower.objects.update_or_create(
                tower_id=tower_id,
                defaults=defaults
            )
            if was_created:
                created += 1
            else:
                updated += 1

    return created, updated

@require_POST
def resolve_tower(request):
    tower_id = request.POST.get("tower_id")
    t = Tower.objects.get(id=tower_id)
    t.operational_status = "Active"
    t.save(update_fields=["operational_status"])
    return JsonResponse({"ok": True})
