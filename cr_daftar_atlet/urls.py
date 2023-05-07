from django.urls import path
from cr_daftar_atlet.views import show_render

app_name = 'cr_daftar_atlet'

urlpatterns = [
    path('', show_render, name='show_render'),
]
