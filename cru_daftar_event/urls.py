from django.urls import path
from cru_daftar_event.views import *

app_name = 'cru_daftar_event'

urlpatterns = [
    path('', cru_daftar_event_views, name='cru_daftar_event_views'),
    path('2/', cru_daftar_event_views_2, name='cru_daftar_event_views_2'),
    path('3/', cru_daftar_event_views_3, name='cru_daftar_event_views_3'),


]