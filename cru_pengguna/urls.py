from django.urls import path
from cru_pengguna.views import *

app_name = 'pengguna'

urlpatterns = [
    path('', show_user, name='show_dashboard'),
    path('atlet/', register_atlet, name='register_atlet'),
    path('pelatih/', register_pelatih, name='register_pelatih'),
    path('umpire/', register_umpire, name='register_umpire'),
]
