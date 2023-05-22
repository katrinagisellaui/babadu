from django.shortcuts import render

# Create your views here.
from rd_enrolled_event.models import *

# Create your views here.
def rd_enrolled_event_view(request):
    return render(request, "rd_enrolled_event.html")