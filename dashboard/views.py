from django.shortcuts import render
from django.db import connection
import psycopg2

# Create your views here.


def show_dashboard(request):
    return render(request, 'dashboard.html')


def show_dashboard_pelatih(request):
    return render(request, 'dashboard_pelatih.html')


def show_dashboard_umpire(request):
    return render(request, 'dashboard_umpire.html')


def show_forbidden(request):
    return render(request, 'forbidden.html')
