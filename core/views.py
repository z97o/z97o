# core/views.py
from django.http import JsonResponse
from .models import Region, Tower, Complaint

def health(request):
    return JsonResponse({"status": "ok"})

def region_list(request):
    data = list(Region.objects.values("id", "name", "code"))
    return JsonResponse(data, safe=False)

def tower_list(request):
    data = list(
        Tower.objects.select_related("region").values(
            "id", "tower_id", "status", "latitude", "longitude",
            "region_id", "region__name", "region__code",
        )
    )
    return JsonResponse(data, safe=False)

def complaint_list(request):
    data = list(
        Complaint.objects.select_related("region", "tower").values(
            "id", "created_at", "category", "status",
            "customer_msisdn",
            "region_id", "region__name", "region__code",
            "tower_id", "tower__tower_id",
        )
    )
    return JsonResponse(data, safe=False)
