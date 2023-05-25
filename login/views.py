from django.db import connection
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime

# Create your views here.


def login_home(request):
    return render(request, "login.html")


# def pilih_login(request):
#     return render(request, "pilih_login.html")


def login(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        email = request.POST.get("email")

        print(nama)
        print(email)

        c = connection.cursor()
        c.execute("SELECT ID FROM MEMBER WHERE EMAIL='{}' AND NAMA = '{}'".format(
            email, nama))
        myuuid = c.fetchone()
        print(myuuid)

        if myuuid is not None:
            myuuid = myuuid[0]
            c.execute("SELECT * FROM ATLET WHERE id = '{}'".format(myuuid))
            atlet = c.fetchone()
            print(atlet)

            c.execute("SELECT * FROM UMPIRE WHERE id = '{}'".format(myuuid))
            umpire = c.fetchone()
            print(umpire)

            c.execute("SELECT * FROM PELATIH WHERE id = '{}'".format(myuuid))
            pelatih = c.fetchone()
            print(pelatih)

            role = None
            response = HttpResponseRedirect(reverse("login:login"))
            if (atlet != None):
                c.execute(
                    "SELECT * FROM ATLET_NON_KUALIFIKASI WHERE id_atlet = '{}'".format(myuuid))
                atlet = c.fetchone()
                print(atlet)
                if (atlet == None):
                    response = HttpResponseRedirect(
                        reverse("dashboard:show_dashboard"))
                    role = "ATLET"
                    print("halo atlet")
                else:
                    response = HttpResponseRedirect(
                        reverse("dashboard:show_dashboard"))
                    role = "ATLET-NON"
                    print("halo atlet non")
            if (pelatih != None):
                response = HttpResponseRedirect(
                    reverse("dashboard:show_dashboard_pelatih"))
                print("halo pelatih")
                role = "PELATIH"
            if (umpire != None):

                response = HttpResponseRedirect(
                    reverse("dashboard:show_dashboard_umpire"))
                print("halo ump")
                role = "UMPIRE"

            response.set_cookie("nama", nama)
            response.set_cookie("id", myuuid)
            response.set_cookie("email", email)
            response.set_cookie("role", role)

            print(response.cookies.get('nama'))
            print(response.cookies.get('id'))
            print(response.cookies.get('email'))
            print(response.cookies.get("role"))

            messages.success(request, "Login success!")
            return response
        else:
            messages.error(
                request, "Nama atau Email yang digunakan untuk Login belum sesuai!")

    return render(request, "pilih_login.html")


def logout_user(request):
    response = HttpResponseRedirect(reverse("login:login_home"))
    response.delete_cookie("nama")
    response.delete_cookie("id")
    response.delete_cookie("email")
    response.delete_cookie("role")
    messages.success(request, "Logout success!")
    return response
