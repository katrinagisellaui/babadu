from django.shortcuts import render
from django.db import connection
import psycopg2

# Create your views here.


def show_dashboard(request):
    cursor = connection.cursor()
    query_select = """
    SELECT *
    FROM ATLET A, POINT_HISTORY P
    WHERE A.id = %s AND A.id = P.id_atlet
    """

    query_select_2 = """
    SELECT MAX(P.total_point)
    FROM ATLET A, POINT_HISTORY P
    WHERE A.id = %s AND A.id = P.id_atlet
    """

    query_select_3 = """
    SELECT M.nama
    FROM ATLET_PELATIH AP, PELATIH P, MEMBER M
    WHERE AP.ID_ATLET = %s AND AP.ID_pelatih = P.ID AND P.ID = M.ID
    """

    query_select_4 = """
    SELECT ID_Atlet
    FROM ATLET_KUALIFIKASI AK
    WHERE AK.ID_ATLET = %s
    """

    nama = request.COOKIES.get("nama")
    email = request.COOKIES.get("email")
    cursor.execute(query_select, (request.COOKIES.get("id"),))
    data_atlet = cursor.fetchall()[0]
    cursor.execute(query_select_2, (request.COOKIES.get("id"),))
    poin = cursor.fetchone()[0]
    cursor.execute(query_select_3, (request.COOKIES.get("id"),))
    nama_pelatih = cursor.fetchone()[0]
    cursor.execute(query_select_4, (request.COOKIES.get("id"),))
    status = cursor.fetchone()[0]
    if (status is None):
        status = "Not Qualified"
    else :
        status = "Qualified"
    context = {"data_atlet":data_atlet, "nama":nama, "email":email, "poin":poin, "pelatih":nama_pelatih
               ,"status":status}
    return render(request, 'dashboard.html', context=context)


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
