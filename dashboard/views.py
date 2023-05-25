from django.shortcuts import render
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


def show_dashboard(request):
    if (request.COOKIES.get('id') == None):
        return redirect("dashboard:show_forbidden")
    nama = request.COOKIES.get("nama")
    email = request.COOKIES.get("email")
    role = request.COOKIES.get("role")
    myid = request.COOKIES.get("id")

    print(nama)
    print(email)
    print(role)

    context = {}

    if (role == "ATLET"):
        c = connection.cursor()
        c.execute("SELECT * FROM ATLET WHERE ID = '{}'".format(myid))
        response = c.fetchall()
        print(response)
        print(response[0][0])
        print(response[0][1])

        tanggal = response[0][1]
        negara = response[0][2]
        play = response[0][3]
        height = response[0][4]
        rank = response[0][5]
        gender = response[0][6]

        c.execute(
            "SELECT DISTINCT * FROM POINT_HISTORY WHERE id_atlet = '{}' ORDER BY tahun desc, bulan desc, minggu_ke desc;".format(myid))
        response = c.fetchall()

        point = response[0][4]

        context = {
            "nama": nama,
            "email": email,
            "tanggal": tanggal,
            "negara": negara,
            "play": play,
            "height": height,
            "rank": rank,
            "gender": gender,
            "status": "Qualified",
            "poin": point,
            "role": role

        }
        return render(request, 'dashboard.html', context)
    else:
        c = connection.cursor()
        c.execute("SELECT * FROM ATLET WHERE ID = '{}'".format(myid))
        response = c.fetchall()
        print(response)
        print(response[0][0])
        print(response[0][1])

        tanggal = response[0][1]
        negara = response[0][2]
        play = response[0][3]
        height = response[0][4]
        rank = response[0][5]
        gender = response[0][6]

        point = 0

        context = {
            "nama": nama,
            "email": email,
            "tanggal": tanggal,
            "negara": negara,
            "play": play,
            "height": height,
            "rank": rank,
            "gender": gender,
            "status": "Not Qualified",
            "poin": point,
            "role": role

        }
        return render(request, 'dashboard.html', context)


def show_dashboard_pelatih(request):
    # if (request.COOKIES.get('id') == None):
    #     return redirect("dashboard:show_forbidden")
    # nama = request.COOKIES.get("nama")
    # email = request.COOKIES.get("email")
    # role = request.COOKIES.get("role")
    # myid = request.COOKIES.get("id")

    # print(nama)
    # print(email)
    # print(role)

    # context = {}
    # c = connection.cursor()
    # c.execute("SELECT * FROM ATLET WHERE ID = '{}'".format(myid))
    # response = c.fetchall()
    # print(response)
    # print(response[0][0])
    # print(response[0][1])

    # tanggal = response[0][1]
    # negara = response[0][2]
    # play = response[0][3]
    # height = response[0][4]
    # rank = response[0][5]
    # gender = response[0][6]

    # point = 0

    # context = {
    #     "nama": nama,
    #     "email": email,
    #     "tanggal": tanggal,
    #     "negara": negara,
    #     "play": play,
    #     "height": height,
    #     "rank": rank,
    #     "gender": gender,
    #     "status": "Not Qualified",
    #     "poin": point,
    #     "role": role

    # }
    return render(request, 'dashboard_pelatih.html')


def show_dashboard_umpire(request):
    return render(request, 'dashboard_umpire.html')


def show_forbidden(request):
    return render(request, 'forbidden.html')
