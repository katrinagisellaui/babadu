from django.urls import path
from c_daftar_sponsor.views import show_render

app_name = 'c_daftar_sponsor'

urlpatterns = [
    path('', show_render, name='show_render'),
]
