from django.db import connection
from django.shortcuts import redirect, render

from django.contrib import messages

# Create your views here.
from rd_enrolled_event.models import *
from datetime import date

# Create your views here.


def rd_enrolled_event_view(request):
    return render(request, "rd_enrolled_event.html")


def rd_enrolled_event_view(request):

    if (request.COOKIES.get('id') == None):
        return redirect("dashboard:show_forbidden")

    # print(request.COOKIES.get('nama'))
    # print(request.COOKIES.get('email'))
    # print(request.COOKIES.get('id'))

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
        # print(np)
        cursor.execute("SELECT pme.nomor_peserta, pme.nama_event, pme.tahun, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai \
                       FROM PESERTA_MENDAFTAR_EVENT pme, EVENT e\
                       WHERE pme.nomor_peserta = {}\
                       AND pme.tahun = e.tahun\
                       AND pme.nama_event = e.nama_event;".format(np[0]))
        enrolled = cursor.fetchall()
        for e in enrolled:
            enrolled_list.append(e)

    # print(enrolled_list)

    context = {"enrolled_list": enrolled_list}
    return render(request, "rd_enrolled_event.html", context)


def delete_enrolled(request, no_peserta, event, tahun):
    print(no_peserta)
    print(event)
    print(tahun)

    print(date.today())

    c = connection.cursor()
    c.execute("CREATE OR REPLACE FUNCTION unenroll()\
              RETURNS trigger AS $$\
              DECLARE tanggal_mulai_event DATE;\
              DECLARE tanggal_selesai_event DATE;\
              BEGIN\
              IF (TG_OP = 'DELETE') THEN\
              SELECT e.tgl_mulai into tanggal_mulai_event\
              FROM EVENT e\
              WHERE e.nama_event = '{}' and e.tahun = {};\
              SELECT e.tgl_selesai into tanggal_selesai_event\
              FROM EVENT e\
              WHERE e.nama_event = '{}' and e.tahun = {};\
              IF(tanggal_mulai_event <= '{}' OR tanggal_selesai_event <= '{}') THEN\
              RAISE EXCEPTION 'Maaf event sudah berjalan / selesai';\
              END IF;\
              END IF; RETURN OLD; END;$$LANGUAGE plpgsql;\
              CREATE OR REPLACE TRIGGER check_unenroll\
              BEFORE DELETE ON PESERTA_MENDAFTAR_EVENT FOR EACH ROW\
              EXECUTE PROCEDURE unenroll();".format(event, tahun, event, tahun, date.today(), date.today()))

    try:
        c.execute("Delete from peserta_mendaftar_event\
                where nomor_peserta = {}\
                and nama_event = '{}'\
                and tahun = {};".format(no_peserta, event, tahun))

        c.execute("Delete from partai_peserta_kompetisi\
                where nomor_peserta = {}\
                and nama_event = '{}'\
                and tahun_event = {};".format(no_peserta, event, tahun))
    except:
        messages.warning(request, 'Maaf event sudah berjalan / selesai')
        print('Maaf event sudah berjalan / selesai')

    return redirect("rd_enrolled_event:rd_enrolled_event_view")
