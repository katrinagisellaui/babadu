from django.shortcuts import render
from cr_daftar_atlet.models import BarangWishlist

from datetime import datetime

# Create your views here.


def pertandingan_berlangsung(request, jenis_match):
    # tanggal = datetime.strptime(tanggal, '%Y-%m-%d').date()
    # waktu_mulai = datetime.strptime(waktu_mulai, '%H:%M:%S').timestamp()
    context = {
        "jenis_match": jenis_match,
        # "tanggal": tanggal,
        # "waktu_mulai": waktu_mulai,
    }
    return render(request, "pertandingan.html", context)

def pertandingan_selesai(request):
    context = {

    }
    return render(request, "event-selesai.html", context)


def hasil_pertandingan(request, nama_event):
    context = {
        "nama_event": nama_event,
    }
    return render(request, "hasil-pertandingan.html", context)
