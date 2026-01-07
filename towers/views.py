# towers/views.py
from django.shortcuts import render
try:
    from .models import Tower
except Exception:
    Tower = None

def index(request):
    towers = Tower.objects.all() if Tower else []
    return render(request, "towers/index.html", {"towers": towers})
