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
    return render(request, 'dashboard_pelatih.html')


def show_dashboard_umpire(request):
    return render(request, 'dashboard_umpire.html')


def show_forbidden(request):
    return render(request, 'forbidden.html')
