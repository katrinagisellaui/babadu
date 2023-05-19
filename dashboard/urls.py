from django.urls import path
from dashboard.views import show_dashboard, show_dashboard_pelatih, show_dashboard_umpire

app_name = 'dashboard'

urlpatterns = [
    path('atlet/', show_dashboard, name='show_dashboard'),
    path('pelatih/', show_dashboard_pelatih, name = 'show_dashboard_pelatih'),
    path('umpire/', show_dashboard_umpire, name='show_dashboard_umpire'),
]