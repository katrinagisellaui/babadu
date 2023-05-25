from django.db import connection
from django.shortcuts import render, redirect
from cr_daftar_atlet.models import *

# Create your views here.
def get_daftar_atlet(request):
    
    # atlet_kualif = AtletKualif.objects.all()
    cursor = connection.cursor()
    cursor.execute("SELECT m.nama, a.tgl_lahir, a.negara_asal, a.play_right, a.height, a.world_rank, ak.world_tour_rank, a.jenis_kelamin, MAX(p.total_point) AS highest_point\
                    FROM member m\
                    JOIN atlet a ON a.id = m.id\
                    JOIN atlet_kualifikasi ak ON ak.id_atlet = m.id\
                    JOIN point_history p ON p.id_atlet = m.id\
                    GROUP BY m.nama, a.tgl_lahir, a.negara_asal, a.play_right, a.height, a.world_rank, ak.world_tour_rank, a.jenis_kelamin;\
                    ")  # add where sponsor user login
    atlet_kualif = cursor.fetchall()
    

    cursor = connection.cursor()
    cursor.execute("SELECT distinct m.nama, a.tgl_lahir, a.negara_asal, a.play_right,\
                    a.height, a.world_rank, a.jenis_kelamin, p.total_point\
                    from member m\
                    join atlet a on a.id = m.id\
                    join atlet_non_kualifikasi an on an.id_atlet = m.id\
                    join point_history  p on p.id_atlet = m.id;")  # add where sponsor user login
    atlet_non_kualif = cursor.fetchall()

    cursor = connection.cursor()
    cursor.execute("select ag.id_atlet_ganda, m1.nama, m2.nama, max(p1.total_point) + max(p2.total_point)\
                    from atlet_ganda ag\
                    join member m1 on m1.id = ag.id_atlet_kualifikasi\
                    join member m2 on m2.id = ag.id_atlet_kualifikasi_2\
                    join point_history p1 on p1.id_atlet = m1.id\
                    join point_history p2 on p2.id_atlet = m2.id\
                    GROUP BY ag.id_atlet_ganda, m1.nama, m2.nama    \
                    ;") 
    atlet_ganda = cursor.fetchall()



    context = {"atlet_kualif_list": atlet_kualif, "atlet_nonkualif_list": atlet_non_kualif, "atlet_ganda_list": atlet_ganda}

    return render(request, "list-atlet.html", context)