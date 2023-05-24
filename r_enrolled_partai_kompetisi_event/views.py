from django.db import connection
from django.shortcuts import redirect, render

from django.contrib import messages
# Create your views here.


def show_list(request):
    if (request.COOKIES.get('id') == None):
        return redirect("dashboard:show_forbidden")

    print(request.COOKIES.get('nama'))
    print(request.COOKIES.get('email'))
    print(request.COOKIES.get('id'))

    myid = request.COOKIES.get('id')
    nama = request.COOKIES.get('nama')
    email = request.COOKIES.get('email')

    cursor = connection.cursor()
    cursor.execute("SELECT nomor_peserta  \
                   FROM PESERTA_KOMPETISI\
                   WHERE id_atlet_kualifikasi = '{}'".format(myid))
    nomor_peserta = cursor.fetchall()

    # print(nomor_peserta)
    # print(nomor_peserta[0][0])

    enrolled_list = []

    for np in nomor_peserta:
        print(np)
        cursor.execute("SELECT pk.nama_event, e.tahun, e.nama_stadium, pk.jenis_partai, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai\
                FROM PARTAI_KOMPETISI pk, PARTAI_PESERTA_KOMPETISI ppk, EVENT e\
                WHERE ppk.nomor_peserta = {}\
                AND pk.jenis_partai = ppk.jenis_partai\
                AND pk.nama_event = ppk.nama_event\
                AND pk.tahun_event = ppk.tahun_event\
                AND pk.tahun_event = e.tahun\
                AND pk.nama_event = e.nama_event;".format(np[0]))
        enrolled = cursor.fetchall()
        for e in enrolled:
            enrolled_list.append(e)

    print(enrolled_list)

    context = {"enrolled_list": enrolled_list}
    return render(request, "r_enrolled_partai.html", context)
