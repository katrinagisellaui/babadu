from django.db import connection
from django.shortcuts import redirect, render

from django.contrib import messages


# Create your views here.


def show_render(request):
    if request.method == "POST":
        id_sponsor = request.POST.get("sponsorDropdown")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        myid = request.COOKIES.get('id')

        print(id_sponsor)
        print(startDate)
        print(endDate)

        c = connection.cursor()
        c.execute("INSERT INTO ATLET_SPONSOR \
                  (id_sponsor, id_atlet, tgl_mulai, tgl_selesai)\
                  VALUES ('{}','{}','{}','{}')".format(id_sponsor, myid, startDate, endDate))

        # messages.success(request, "Sponsorship telah berhasil dibuat!")
        return redirect("c_daftar_sponsor:show_list")

    if (request.COOKIES.get('id') == None):
        return redirect("dashboard:show_forbidden")

    myid = request.COOKIES.get('id')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SPONSOR\
                   WHERE ID NOT IN (\
                   SELECT ID_Sponsor\
                   FROM ATLET_SPONSOR\
                   WHERE ID_ATLET = '{}');".format(myid))
    sponsor = cursor.fetchall()

    context = {"sponsor_list": sponsor}
    return render(request, "daftar-sponsor.html", context)


def show_list(request):
    if (request.COOKIES.get('id') == None):
        return redirect("dashboard:show_forbidden")

    print(request.COOKIES.get('nama'))
    print(request.COOKIES.get('email'))
    print(request.COOKIES.get('id'))

    myid = request.COOKIES.get('id')
    nama = request.COOKIES.get('nama')
    email = request.COOKIES.get('email')

    if (myid == None or nama == None or email == None):
        return render(request, "forbidden.html")

    cursor = connection.cursor()
    cursor.execute("SELECT nama_brand, tgl_mulai, tgl_selesai \
                   FROM sponsor, atlet_sponsor\
                   WHERE id_sponsor = id\
                   AND id_atlet = '{}'".format(myid))
    sponsor = cursor.fetchall()

    context = {"sponsor_list": sponsor}
    return render(request, "list-sponsor.html", context)
