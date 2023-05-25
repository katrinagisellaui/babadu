from django.urls import path
from cru_daftar_event.views import *

app_name = 'cru_daftar_event'

urlpatterns = [
    path('', daftar_stadium, name='daftar_stadium'),
    path('daftar_event/<str:nama_stadium>/', daftar_event, name='daftar_event'),
    path('daftar_event/<str:nama_stadium>/<str:nama_event>/<int:tahun_event>/', daftar_partai, name='daftar_partai'),
]