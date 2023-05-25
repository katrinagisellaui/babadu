from django.urls import path
from cr_daftar_atlet.views import *

app_name = 'cr_daftar_atlet'

urlpatterns = [
    path('', show_render, name='show_render'),
    path('list/', get_atlet_kualifikasi, name="get_atlet_kualifikasi"),
    path('c-latih-atlet/', c_latih_atlet, name="c_latih_atlet"),
    path('r-latih-atlet/', r_latih_atlet, name="r_latih_atlet")

]
