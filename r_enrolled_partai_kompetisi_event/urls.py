from django.urls import path
from r_enrolled_partai_kompetisi_event.views import *

app_name = 'r_enrolled_partai_kompetisi_event'

urlpatterns = [
    path('', show_list, name='show_list'),
]
