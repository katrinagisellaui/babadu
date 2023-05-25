from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.db import connection
import uuid

# Create your views here.


def show_user(request):
    return render(request, 'pengguna.html')


def show_atlet(request):
    return render(request, 'atlet.html')


def show_pelatih(request):
    return render(request, 'pelatih.html')


def show_umpire(request):
    return render(request, 'umpire.html')


def register_atlet(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        negara = request.POST.get("negara")
        birth = request.POST.get("birth")
        play = request.POST["play"]
        gender = request.POST["gender"]
        tinggi = request.POST.get("tinggi")

        print(nama)
        print(email)
        print(negara)
        print(birth)
        print(play)
        print(gender)
        print(tinggi)

        myuuid = uuid.uuid1()
        play_bool = False
        gender_bool = False

        if (play == "Right"):
            play_bool = True

        if (gender == "Laki"):
            gender_bool = True

        print(gender_bool)
        print(play_bool)
        print(myuuid)

        c = connection.cursor()
        c.execute("INSERT INTO MEMBER VALUES ('{}','{}','{}')".format(
            myuuid, nama, email))
        c.execute("INSERT INTO ATLET \
                  (id, tgl_lahir, Negara_Asal, play_right, height, jenis_kelamin)\
                  VALUES ('{}','{}','{}','{}','{}', '{}')".format(
            myuuid, birth, negara, play_bool, tinggi, gender_bool))

        c.execute("INSERT INTO ATLET_NON_KUALIFIKASI \
                VALUES ('{}')".format(
            myuuid))

        messages.success(request, "Akun Atlet telah berhasil dibuat!")
        return redirect("login:login_home")

    return render(request, "atlet.html")


def register_umpire(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        negara = request.POST.get("negara")

        print(nama)
        print(email)
        print(negara)

        myuuid = uuid.uuid1()

        print(myuuid)

        c = connection.cursor()
        c.execute("INSERT INTO MEMBER VALUES ('{}','{}','{}')".format(
            myuuid, nama, email))
        c.execute("INSERT INTO UMPIRE \
                  (id, negara)\
                  VALUES ('{}','{}')".format(
            myuuid, negara))

        messages.success(request, "Akun Umpire telah berhasil dibuat!")
        return redirect("login:login_home")

    return render(request, "umpire.html")


def register_pelatih(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        kategori = request.POST.getlist('kategori')
        date = request.POST.get("date")

        print(nama)
        print(email)
        print(kategori)
        print(date)

        myuuid = uuid.uuid1()

        print(myuuid)

        c = connection.cursor()
        c.execute("INSERT INTO MEMBER VALUES ('{}','{}','{}')".format(
            myuuid, nama, email))
        c.execute("INSERT INTO PELATIH \
                  (id, tanggal_mulai)\
                  VALUES ('{}','{}')".format(
            myuuid, date))

        for k in kategori:
            c.execute("INSERT INTO PELATIH_SPESIALISASI \
                    (id_pelatih, id_spesialisasi)\
                    VALUES ('{}','{}')".format(
                myuuid, k))

        messages.success(request, "Akun Pelatih telah berhasil dibuat!")
        return redirect("login:login_home")

    return render(request, "pelatih.html")
