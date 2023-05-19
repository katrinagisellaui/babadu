from django.shortcuts import render

# Create your views here.
def show_user(request) :
    return render(request, 'pengguna.html')

def show_atlet(request) :
    return render(request, 'atlet.html')

def show_pelatih(request) :
    return render(request, 'pelatih.html')

def show_umpire(request) :
    return render(request, 'umpire.html')