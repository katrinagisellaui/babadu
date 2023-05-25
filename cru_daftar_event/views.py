from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
import psycopg2
import locale
import uuid
locale.setlocale(locale.LC_ALL, '')
# Create your views here.
from cru_daftar_event.models import *

# Create your views here.
def cru_daftar_event_views(request):
    return render(request, "cru_daftar_event_1.html")

def cru_daftar_event_views_2(request):
    return render(request, "cru_daftar_event_2.html")

def cru_daftar_event_views_3(request):
    return render(request, "cru_daftar_event_3.html")

def connect_db():
    db_connection = psycopg2.connect(
        host="containers-us-west-128.railway.app",
        database="railway",
        user="postgres",
        password="uerDeirCf7NJNyoYqW5Q",
        port="6881",
    )
    return db_connection

def search_path():
    return """SET search_path to babadu"""

def daftar_stadium(request):
    context = {}
    query_get_stadium = """
    SELECT * FROM STADIUM;
    """
    db_connection = connect_db()

    cursor = db_connection.cursor()
    cursor.execute(query_get_stadium)
    context['daftar_stadium'] = cursor.fetchall()
    db_connection.close()
    return render(request, 'cru_daftar_event_1.html', context=context)

def daftar_event(request, nama_stadium):
    context = {}
    db_connection = connect_db()
    query_select_event = """
    SELECT E.nama_event, E.total_hadiah, E.tgl_mulai, E.kategori_Superseries, E.tahun
    FROM EVENT E
    WHERE E.tgl_mulai > CURRENT_DATE AND E.nama_stadium = %s
    """
    cursor = db_connection.cursor()
    cursor.execute(query_select_event, (nama_stadium,))
    tuple_event = cursor.fetchall()
    context = {'daftar_event': tuple_event, 'nama_stadium' : nama_stadium}
    db_connection.close()
    return render(request, 'cru_daftar_event_2.html', context=context)

def daftar_partai(request, nama_stadium, nama_event, tahun_event):
    context = {}
    #Ganti pake id atlet login
    id_atlet = request.COOKIES.get("id")
    db_connection = connect_db()
    cursor = db_connection.cursor()
    if (request.method == 'POST'):
        map_partai = {'Tunggal Putra':'TP', 'Tunggal Putri':'TW', 
                              'Ganda Putra':'GP', 'Ganda Putri':'GW', 
                              'Ganda Campuran':'GC'}
        if ('Ganda' in request.POST['jenis']):
            try:
                query_get_pasangan = """
                SELECT id
                FROM MEMBER M
                WHERE M.email = %s
                """
                atlet_rank = get_atlet_rank(id_atlet, cursor)
                jenis_partai = map_partai.get(request.POST['jenis'])
                print(jenis_partai)
                email_pasangan = request.POST['pasangan']
                print(email_pasangan)
                cursor.execute(query_get_pasangan, (email_pasangan,))
                id_pasangan = cursor.fetchone()[0] #pasangan cuma 1
                print(id_pasangan)
                id_atlet_pasangan = get_atlet_ganda_id (id_atlet, id_pasangan, cursor)
                if (id_atlet_pasangan is not None):
                    id_atlet_pasangan = id_atlet_pasangan[0]
                else :
                    id_atlet_pasangan = str(uuid.uuid4())
                    insert_atlet_ganda(id_atlet, id_pasangan, id_atlet_pasangan)
                nomor_peserta = get_nomor_peserta_ganda(cursor,id_atlet_pasangan)
                if (nomor_peserta is not None):
                    nomor_peserta = nomor_peserta[0]
                else:
                    nomor_peserta = insert_peserta_kompetisi(cursor, atlet_rank, None, id_atlet_pasangan)
                insert_partai_peserta_kompetisi(cursor, jenis_partai, nama_event, tahun_event,nomor_peserta)
                db_connection.commit()
                db_connection.close()
                return redirect(request.get_full_path())
            except Exception as e :
                messages.error(request, e)
                db_connection.rollback()
                db_connection.close()
                return redirect(request.get_full_path())
        else :  #Bukan ganda
            try:
                atlet_rank = get_atlet_rank(id_atlet, cursor)
                jenis_partai = map_partai.get(request.POST['jenis'])
                nomor_peserta = get_nomor_peserta_tunggal(cursor, id_atlet)
                if (nomor_peserta is not None):
                    nomor_peserta = nomor_peserta[0]
                else :
                    nomor_peserta = insert_peserta_kompetisi(cursor, atlet_rank, id_atlet, None)
                insert_partai_peserta_kompetisi(cursor, jenis_partai, nama_event, tahun_event, nomor_peserta)
                db_connection.commit()
                db_connection.close()
                return redirect(request.get_full_path())
            except Exception as e:
                messages.error(request, e)
                db_connection.rollback()
                db_connection.close()
                return redirect(request.get_full_path())
    display_event = get_event(nama_event, tahun_event, cursor)
    display_stadium = get_stadium(nama_stadium, cursor)
    display_partai = get_partai(nama_event, tahun_event, id_atlet, cursor)
    display_atlet = get_atlet(id_atlet, cursor)
    display_atlet_ganda = get_atlet_ganda(id_atlet, nama_event, tahun_event, cursor)
    context= {'display_event':display_event, 'display_stadium':display_stadium, 
              'display_partai':display_partai, 'display_atlet':display_atlet,
              'display_atlet_ganda':display_atlet_ganda}
    db_connection.close()
    return render(request, 'cru_daftar_event_3.html', context=context)

def get_event(nama_event, tahun_event, cursor):
    query_list_event = """
    SELECT * 
    FROM EVENT E
    WHERE E.nama_event = %s AND E.tahun = %s
    """
    cursor.execute(query_list_event, (nama_event, tahun_event))
    list_event = cursor.fetchone()
    return list_event

def get_stadium(nama_stadium, cursor):
    query_list_stadium = """
    SELECT *
    FROM STADIUM S
    WHERE S.nama = %s
    """
    cursor.execute(query_list_stadium, (nama_stadium,))
    list_stadium = cursor.fetchone()
    return list_stadium

def get_partai(nama_event, tahun_event, id_atlet, cursor):
    query_list_partai = """
    SELECT P.jenis_partai, COUNT(*) as banyak_pertandingan
    FROM PARTAI_KOMPETISI P
    JOIN EVENT E ON P.nama_event = E.nama_event AND P.tahun_event = E.tahun
    JOIN PARTAI_PESERTA_KOMPETISI PK ON PK.jenis_partai = P.jenis_partai AND PK.nama_event = P.nama_event AND PK.tahun_event = P.tahun_event
    WHERE P.nama_event = %s AND P.tahun_event = %s
    GROUP BY P.jenis_partai, P.nama_event, P.tahun_event;
    """

    query_cek_partai_atlet = """
    SELECT EXISTS (
        (
            SELECT P.id_atlet_kualifikasi
            FROM PARTAI_PESERTA_KOMPETISI PK
            JOIN PESERTA_KOMPETISI P ON PK.Nomor_Peserta = P.Nomor_Peserta
            WHERE PK.jenis_partai = %s AND PK.nama_event = %s AND PK.tahun_event = %s AND P.ID_Atlet_Kualifikasi = %s
        )
        UNION
        (
            SELECT AG.ID_ATLET_KUALIFIKASI
            FROM PARTAI_PESERTA_KOMPETISI PK
            JOIN PESERTA_KOMPETISI P ON PK.Nomor_Peserta = P.Nomor_Peserta
            JOIN ATLET_GANDA AG ON AG.ID_Atlet_Ganda = P.ID_Atlet_Ganda
            WHERE PK.jenis_partai = %s AND PK.nama_event = %s AND PK.tahun_event = %s AND AG.ID_Atlet_Kualifikasi = %s
        )
        UNION
        (
            SELECT AG.ID_ATLET_KUALIFIKASI_2
            FROM PARTAI_PESERTA_KOMPETISI PK
            JOIN PESERTA_KOMPETISI P ON PK.Nomor_Peserta = P.Nomor_Peserta
            JOIN ATLET_GANDA AG ON AG.ID_Atlet_Ganda = P.ID_Atlet_Ganda
            WHERE PK.jenis_partai = %s AND PK.nama_event = %s AND PK.tahun_event = %s AND AG.ID_Atlet_Kualifikasi_2 = %s
        )
    ) AS cek_partai_atlet;
    """

    cursor.execute(query_list_partai, (nama_event, tahun_event))
    list_partai = cursor.fetchall()
    map_partai = {'TP':'Tunggal Putra', 'TW':'Tunggal Putri', 'GP':'Ganda Putra', 'GW':'Ganda Putri', 'GC':'Ganda Campuran'}

    for i in range(len(list_partai)):
        cursor.execute(query_cek_partai_atlet, (list_partai[i][0], nama_event, tahun_event, id_atlet, list_partai[i][0], nama_event, tahun_event, id_atlet, list_partai[i][0], nama_event, tahun_event, id_atlet))
        list_partai[i] = (map_partai.get(list_partai[i][0]), list_partai[i][1], cursor.fetchone()[0])

    return list_partai

def get_atlet(id_atlet, cursor):
    query_get_atlet = """
    SELECT M.nama, A.Jenis_Kelamin
    FROM MEMBER M
    JOIN ATLET A ON M.ID = A.ID
    WHERE M.id = %s
    """
    cursor.execute(query_get_atlet, (id_atlet,))
    info_atlet = cursor.fetchone()
    return info_atlet

def get_atlet_ganda(id_atlet, nama_event, tahun_event, cursor):
    query_get_ganda = """
    SELECT M.nama, A.jenis_kelamin, M.email
    FROM MEMBER M
    JOIN ATLET A ON M.ID = A.ID
    JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.id_atlet
    WHERE A.id <> %s
    AND A.id NOT IN (
        (SELECT AG.id_atlet_kualifikasi
        FROM PARTAI_KOMPETISI P
        JOIN PARTAI_PESERTA_KOMPETISI PPK ON PPK.jenis_partai = P.jenis_partai
                                        AND PPK.nama_event = P.nama_event
                                        AND PPK.tahun_event = P.tahun_event
        JOIN PESERTA_KOMPETISI PK ON PPK.Nomor_Peserta = PK.Nomor_Peserta
        JOIN ATLET_GANDA AG ON PK.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
        WHERE PPK.nama_event = %s
        AND PPK.tahun_event = %s)
        UNION
        (SELECT AG.id_atlet_kualifikasi
        FROM PARTAI_KOMPETISI P
        JOIN PARTAI_PESERTA_KOMPETISI PPK ON PPK.jenis_partai = P.jenis_partai
                                        AND PPK.nama_event = P.nama_event
                                        AND PPK.tahun_event = P.tahun_event
        JOIN PESERTA_KOMPETISI PK ON PPK.Nomor_Peserta = PK.Nomor_Peserta
        JOIN ATLET_GANDA AG ON PK.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
        WHERE PPK.nama_event = %s
        AND PPK.tahun_event = %s)
    );
    """
    cursor.execute(query_get_ganda, (id_atlet, nama_event, tahun_event, nama_event, tahun_event))
    info_atlet_ganda = cursor.fetchall()
    return info_atlet_ganda

def get_atlet_ganda_id(id_atlet, id_pasangan, cursor):
    query_get_pasangan_id = """
    SELECT A.id_atlet_ganda
    FROM ATLET_GANDA A
    WHERE (A.id_atlet_kualifikasi = %s AND A.id_atlet_kualifikasi_2 = %s) OR (A.id_atlet_kualifikasi_2 = %s AND A.id_atlet_kualifikasi = %s)
    """
    cursor.execute(query_get_pasangan_id, (id_atlet, id_pasangan, id_atlet, id_pasangan))
    result = cursor.fetchone()
    return result

def get_atlet_rank(id_atlet, cursor):
    query_get_rank = """
    SELECT A.world_rank, A.world_tour_rank
    FROM ATLET_KUALIFIKASI A
    WHERE A.id_atlet = %s
    """
    cursor.execute(query_get_rank, (id_atlet,))
    atlet_rank = cursor.fetchone()
    return atlet_rank

def get_nomor_peserta_ganda(cursor, id_atlet_ganda):
    query_get_nomor_peserta = """
                SELECT P.nomor_peserta
                FROM PESERTA_KOMPETISI P
                WHERE P.id_atlet_ganda = %s
                """
    cursor.execute(query_get_nomor_peserta, (id_atlet_ganda,))
    nomor_peserta = cursor.fetchone()
    return nomor_peserta

def get_nomor_peserta_tunggal(cursor, id_atlet):
    query_select = """
    SELECT P.nomor_peserta
    FROM PESERTA_KOMPETISI P
    WHERE P.id_atlet_kualifikasi = %s
    """
    cursor.execute(query_select, (id_atlet,))
    nomor_peserta = cursor.fetchone()
    return nomor_peserta

def insert_atlet_ganda(id_atlet, id_pasangan, id_atlet_ganda, cursor):
    query_insert_ganda = """
    INSERT INTO ATLET_GANDA (id_atlet_ganda, id_atlet_kualifikasi, id_atlet_kualifikasi_2)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query_insert_ganda(id_atlet_ganda, id_atlet, id_pasangan))

def insert_peserta_kompetisi(cursor, atlet_rank, id_atlet_kualifikasi, id_atlet_ganda):
    query_nomor_peserta = """
    SELECT MAX(P.nomor_peserta)+1 as Nomor_peserta
    FROM PESERTA_KOMPETISI P
    """
    query_insert = """
    INSERT INTO PESERTA_KOMPETISI (Nomor_Peserta, ID_Atlet_Ganda, ID_Atlet_Kualifikasi, World_Rank, World_Tour_Rank) 
    VALUES (%s,%s,%s,%s,%s)
    """
    cursor.execute(query_nomor_peserta)
    nomor_peserta = cursor.fetchone()[0]
    cursor.execute(query_insert, (nomor_peserta, id_atlet_ganda, id_atlet_kualifikasi, atlet_rank[0], atlet_rank[1]))
    return nomor_peserta

def insert_partai_peserta_kompetisi(cursor, jenis_partai, nama_event, tahun_event, nomor_peserta):
    query_insert = """
    INSERT INTO PARTAI_PESERTA_KOMPETISI (Jenis_Partai, Nama_Event, Tahun_Event, Nomor_Peserta) 
    VALUES (%s,%s,%s,%s) 
    """
    cursor.execute(query_insert, (jenis_partai, nama_event, tahun_event, nomor_peserta))

