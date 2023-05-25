from django.urls import path
from cru_tes_kualif_atlet.views import \
    show_render, show_create_ujian, list_ujian, create_ujian, ujian_atlet, submit_ujian, riwayat_ujian

app_name = 'cru_tes_kualif_atlet'

urlpatterns = [
    path('', show_render, name='home'),
    path('list-ujian/', list_ujian, name='list-ujian'),
    path('create-ujian/', show_create_ujian, name='create-ujian'),
    path('submit-new-ujian/', create_ujian, name='submit-new-ujian'),
    path('ujian/', ujian_atlet, name='ujian-atlet'),
    path('submit-ujian/', submit_ujian, name='submit-ujian'),
    path('riwayat/', riwayat_ujian, name='riwayat'),

]
