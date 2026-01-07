from django.shortcuts import render
from .models import Region
def index(request):
    return render(request, "regions/index.html", {"regions": Region.objects.all()})
