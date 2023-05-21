from django.urls import path
from rd_enrolled_event.views import *

app_name = 'rd_enrolled_event'

urlpatterns = [
    path('', rd_enrolled_event_view, name='rd_enrolled_event_view'),
]