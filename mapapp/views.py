from django.shortcuts import render

def signal_map(request):
    return render(request, "mapapp/signal_map.html")
