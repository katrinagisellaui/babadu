from django.urls import path
from cru_pengguna.views import show_user, show_atlet, show_pelatih, show_umpire

app_name = 'pengguna'

urlpatterns = [
    path('', show_user, name='show_dashboard'),
    path('atlet/', show_atlet, name='show_atlet'),
    path('pelatih/', show_pelatih, name='show_pelatih'),
    path('umpire/', show_umpire, name='show_umpire'),
]