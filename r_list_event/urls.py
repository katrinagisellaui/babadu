from django.urls import path
from r_list_event.views import *

app_name = 'r_list_event'

urlpatterns = [
    path('', r_list_event_view, name='r_list_event_view'),
]
