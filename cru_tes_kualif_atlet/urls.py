from django.urls import path
from cru_tes_kualif_atlet.views import show_render

app_name = 'cru_tes_kualif_atlet'

urlpatterns = [
    path('', show_render, name='show_render'),
]
