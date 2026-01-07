from django.shortcuts import render
from django.db.models import Count

# Try to import models safely
try:
    from complaints.models import Complaint
except Exception:
    Complaint = None

try:
    from regions.models import Region
except Exception:
    Region = None

try:
    from towers.models import Tower
except Exception:
    Tower = None

def index(request):
    # Dashboard counts (fallback demo numbers)
    regions_count = Region.objects.count() if Region else 12
    towers_count = Tower.objects.count() if Tower else 352
    complaints_total = Complaint.objects.count() if Complaint else 108
    complaints_open = Complaint.objects.filter(status='open').count() if Complaint else 15

    def aggregate(field):
        if not Complaint:
            return []
        return list(Complaint.objects.values(field).annotate(count=Count(field)))

    context = {
        "regions_count": regions_count,
        "towers_count": towers_count,
        "complaints_total": complaints_total,
        "complaints_open": complaints_open,
        "status_data": aggregate("status"),
        "priority_data": aggregate("priority"),
        "category_data": aggregate("category"),
    }
    return render(request, "dashboard/index.html", context)
