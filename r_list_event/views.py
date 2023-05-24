from django.shortcuts import render
from r_list_event.models import *

# Create your views here.
def r_list_event_view(request):
    return render(request, "r_list_event.html")