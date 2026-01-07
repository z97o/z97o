from django.shortcuts import render
from .models import Complaint
def index(request):
    return render(request, "complaints/index.html", {"complaints": Complaint.objects.all()})
