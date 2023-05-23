from django.urls import path
from c_daftar_sponsor.views import *

app_name = 'c_daftar_sponsor'

urlpatterns = [
    path('', show_render, name='show_render'),
    path('list', show_list, name='show_list')
]
