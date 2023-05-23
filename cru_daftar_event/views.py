from django.shortcuts import render

# Create your views here.
from cru_daftar_event.models import *

# Create your views here.
def cru_daftar_event_views(request):
    return render(request, "cru_daftar_event_1.html")

def cru_daftar_event_views_2(request):
    return render(request, "cru_daftar_event_2.html")

def cru_daftar_event_views_3(request):
    return render(request, "cru_daftar_event_3.html")

