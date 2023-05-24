from django.urls import path
from pertandingan.views import pertandingan_berlangsung
from pertandingan.views import pertandingan_selesai
from pertandingan.views import hasil_pertandingan

app_name = 'pertandingan'

urlpatterns = [
    # path('<str:jenis_match>/<str:tanggal>/<str:waktu_mulai>', show_render, name='show_render'),
    path('<str:jenis_match>', pertandingan_berlangsung, name='pertandingan_berlangsung'),
    path('selesai/', pertandingan_selesai, name='pertandingan_selesai'),
    path('hasil-pertandingan/<str:nama_event>', hasil_pertandingan, name='hasil_pertandingan'),
]
