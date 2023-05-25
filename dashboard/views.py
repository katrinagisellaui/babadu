from django.shortcuts import render
from django.db import connection
from django.shortcuts import render
from django.db import connection
import psycopg2

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
    cursor = connection.cursor()
    query_select = """
    SELECT P.tanggal_mulai
    FROM PELATIH P
    WHERE P.ID = %s
    """

    query_select_2 = """
    SELECT string_agg(S.spesialisasi, ',')
    FROM SPESIALISASI S, PELATIH_SPESIALISASI P
    WHERE P.id_pelatih = %s AND S.id = P.id_spesialisasi
    """
    nama = request.COOKIES.get("nama")
    email = request.COOKIES.get("email")
    id = request.COOKIES.get("id")
    cursor.execute(query_select, (id, ))
    tanggal_mulai = cursor.fetchone()[0]
    cursor.execute(query_select_2, (id, ))
    spesialisasi = cursor.fetchall()[0][0]
    print(spesialisasi)
    context = {"nama":nama, "email":email, "tanggal_mulai":tanggal_mulai, "spesialisasi":spesialisasi}
    return render(request, 'dashboard_pelatih.html', context=context)


def show_dashboard_umpire(request):
    query_select = """
    SELECT negara
    FROM UMPIRE U
    WHERE U.ID = %s
    """
    cursor = connection.cursor()
    nama = request.COOKIES.get("nama")
    email = request.COOKIES.get("email")
    id = request.COOKIES.get("id")
    cursor.execute(query_select, (id, ))
    negara = cursor.fetchone()[0]
    context = {"nama":nama, "email":email, "negara":negara}
    return render(request, 'dashboard_umpire.html', context=context)


def show_forbidden(request):
    return render(request, 'forbidden.html')
