from django.urls import path
from r_daftar_atlet.views import *

app_name = 'r_daftar_atlet'

urlpatterns = [
    path('', get_daftar_atlet, name='get_daftar_atlet'),

]