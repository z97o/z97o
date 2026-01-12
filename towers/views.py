from django.db.models import Q

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

    total_towers = towers_all.count()  # ✅ يعكس اللي في الداشبورد
    active_count = towers_qs.filter(operational_status__iexact="Active").count()
    maintenance_count = towers_qs.filter(operational_status__iexact="Maintenance").count()
    down_count = towers_qs.filter(operational_status__iexact="Down").count()

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
        "total_towers": total_towers,          # ✅ نفس الداشبورد
        "active_count": active_count,
        "maintenance_count": maintenance_count,
        "down_count": down_count,
        # ✅ تشخيص سريع (مفيد جدًا على Render)
        "mapped_towers": len(towers),
    }
    return render(request, "towers/tower_map.html", context)
