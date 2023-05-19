from django.shortcuts import render

# Create your views here.
def show_render_login(request) :
    return render(request, "login.html")

def show_render_user_login(request) :
    return render(request, "pilih_login.html")