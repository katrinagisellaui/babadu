from django.db import connection
from django.shortcuts import render
from r_list_event.models import *
from urllib.parse import unquote


# Create your views here.
# def r_list_event_view(request):
#     return render(request, "r_list_event.html")

def get_partai_kompetisi(request):
    
    cursor = connection.cursor()
    cursor.execute("\
                    select pk.nama_event, pk.tahun_event, e.nama_stadium, pk.jenis_partai, e.kategori_superseries, e.tgl_mulai, \
                    e.tgl_selesai, count(distinct pme.nomor_peserta), s.kapasitas\
                    from partai_kompetisi pk\
                    join event e on e.nama_event = pk.nama_event\
                    join peserta_mendaftar_event pme on pme.nama_event = e.nama_event and pme.tahun = e.tahun\
                    join stadium s on s.nama = e.nama_stadium\
                    group by pk.nama_event, pk.tahun_event, e.nama_stadium, pk.jenis_partai,e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas;\
    ")
    # cursor.execute("select nama from member;")
    partai_kompetisi_detail = cursor.fetchall();
    # print(partai_kompetisi_detail)

    context = {"partai_kompetisi_detail": partai_kompetisi_detail,}

    return render(request, "r_list_event.html", context)


def lihat_hasil(request, nama_event, tahun_event, jenis_partai):


    cursor = connection.cursor()

    # cursor.execute("\
    # select pk.jenis_partai, pk.nama_event, pk.nama_event, e.nama_stadium, e.total_hadiah, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas\
    # from partai_kompetisi pk, event e, stadium s\
    # where e.nama_event  = pk.nama_event and e.tahun = pk.tahun_event\
    # and s.nama = e.nama_stadium\
    # and pk.nama_event = '{0}' AND pk.jenis_partai = '{1}' AND pk.tahun_event = {2};".format(nama_event, jenis_partai, tahun_event)
    # )

    query_new = """ 
     select pk.jenis_partai, pk.nama_event, pk.nama_event, e.nama_stadium, e.total_hadiah, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai, s.kapasitas
    from partai_kompetisi pk, event e, stadium s
    where e.nama_event  = pk.nama_event and e.tahun = pk.tahun_event
    and s.nama = e.nama_stadium
    and pk.nama_event = %s AND pk.jenis_partai = %s AND pk.tahun_event = %s;
    
    """
    cursor.execute(query_new, (nama_event, jenis_partai, tahun_event))

    hasil_pertandingan_header_fetch = cursor.fetchall()
    hasil_pertandingan_header = []
    for h in hasil_pertandingan_header_fetch:
        hasil_pertandingan_header.append({
            "jenis_partai" : h[0],
            "nama_event_1" : h[1],
            "nama_event_2" : h[2],
            "nama_stadium" : h[3],
            "total_hadiah" : h[4],
            "kategori" : h[5],
            "tgl_mulai" : h[6],
            "tgl_selesi" : h[7],
            "kapasitas" : h[8],

        })
    # hasil_pertandingan_header = ["hello"]

    # print(hasil_pertandingan_header_fetch)
    # print(tahun_event)
    # print(jenis_partai)
    # print(nama_event)

    # untuk juara 1 ganda
    query_juara_1_ganda = """
                        select nama from member me where me.id IN(
                        select a.id from atlet a
                        join atlet_ganda ag on ag.id_atlet_kualifikasi = a.id
                        join peserta_kompetisi pk on ag.id_atlet_ganda = pk.id_atlet_ganda
                        join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
                        join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
                        join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
                        join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
                        join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak = m.jenis_babak and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai
                        where pmm.jenis_babak =  'Final'  and pmm.status_menang = True and e.tahun = %s and e.nama_event = %s and ppk.jenis_partai = %s) OR ID IN
                        (select a.id from atlet a
                        join atlet_ganda ag on ag.id_atlet_kualifikasi_2 = a.id
                        join peserta_kompetisi pk on ag.id_atlet_ganda = pk.id_atlet_ganda
                        join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
                        join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
                        join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
                        join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
                        join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak = m.jenis_babak and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai
                        where pmm.jenis_babak =  'Final'  and pmm.status_menang = True and e.tahun = %s and e.nama_event = %s and ppk.jenis_partai = %s);
                         """

    cursor.execute(query_juara_1_ganda, (tahun_event, nama_event, jenis_partai, tahun_event, nama_event, jenis_partai))
    juara_1_ganda = cursor.fetchall()
    print(juara_1_ganda)

    query_juara_1_tunggal = """ 
    select nama from member me where me.id IN (
        select a.id from atlet a
        join atlet_kualifikasi ak on ak.id_atlet = a.id
        join peserta_kompetisi pk on ak.id_atlet = pk.id_atlet_kualifikasi
        join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
        join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
        join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
        join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
        join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak = m.jenis_babak and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai
        where pmm.jenis_babak = 'Semifinal' and pmm.status_menang = True and e.tahun = %s and e.nama_event = %s and ppk.jenis_partai = %s
    );
    """
    cursor.execute(query_juara_1_tunggal, (tahun_event, nama_event, jenis_partai))

    juara_1_tunggal = cursor.fetchall()

    query_nyoba = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_ganda ag on ag.id_atlet_kualifikasi = a.id
join peserta_kompetisi pk on ag.id_atlet_ganda = pk.id_atlet_ganda
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Final' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = True and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba, (tahun_event, nama_event, jenis_partai))

    nyoba = cursor.fetchall()

    query_nyoba_t = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_kualifikasi ag on ag.id_atlet = a.id
join peserta_kompetisi pk on ag.id_atlet = pk.id_atlet_kualifikasi
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Final' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = True and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba, (tahun_event, nama_event, jenis_partai))

    nyoba_t = cursor.fetchall()

    query_nyoba_2 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_ganda ag on ag.id_atlet_kualifikasi = a.id
join peserta_kompetisi pk on ag.id_atlet_ganda = pk.id_atlet_ganda
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Final' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = False and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba_2, (tahun_event, nama_event, jenis_partai))

    nyoba_2 = cursor.fetchall()

    query_nyoba_t_2 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_kualifikasi ag on ag.id_atlet = a.id
join peserta_kompetisi pk on ag.id_atlet = pk.id_atlet_kualifikasi
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Final' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = False and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba, (tahun_event, nama_event, jenis_partai))

    nyoba_t_2 = cursor.fetchall()

    query_nyoba_3 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_ganda ag on ag.id_atlet_kualifikasi = a.id
join peserta_kompetisi pk on ag.id_atlet_ganda = pk.id_atlet_ganda
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Semifinal' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = True and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba_3, (tahun_event, nama_event, jenis_partai))

    nyoba_3 = cursor.fetchall()

    query_nyoba_t_3 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_kualifikasi ag on ag.id_atlet = a.id
join peserta_kompetisi pk on ag.id_atlet = pk.id_atlet_kualifikasi
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Semifinal' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = True and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba, (tahun_event, nama_event, jenis_partai))

    nyoba_t_3 = cursor.fetchall()

    query_nyoba_4 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_ganda ag on ag.id_atlet_kualifikasi = a.id
join peserta_kompetisi pk on ag.id_atlet_ganda = pk.id_atlet_ganda
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Semifinal' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = False and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba_4, (tahun_event, nama_event, jenis_partai))

    nyoba_4 = cursor.fetchall()

    query_nyoba_t_3 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_kualifikasi ag on ag.id_atlet = a.id
join peserta_kompetisi pk on ag.id_atlet = pk.id_atlet_kualifikasi
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'Semifinal' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = False and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba, (tahun_event, nama_event, jenis_partai))

    nyoba_t_4 = cursor.fetchall()

    query_nyoba_5 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_ganda ag on ag.id_atlet_kualifikasi = a.id
join peserta_kompetisi pk on ag.id_atlet_ganda = pk.id_atlet_ganda
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'R16' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = False and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba_5, (tahun_event, nama_event, jenis_partai))

    nyoba_5 = cursor.fetchall()

    query_nyoba_t_5 = """ 
    select me.nama from member me
join atlet a on a.id = me.id 
join atlet_kualifikasi ag on ag.id_atlet = a.id
join peserta_kompetisi pk on ag.id_atlet = pk.id_atlet_kualifikasi
join partai_peserta_kompetisi ppk on ppk.nomor_peserta = pk.nomor_peserta
join event e on e.nama_event = ppk.nama_event and e.tahun = ppk.tahun_event
join peserta_mendaftar_event pme on pme.nomor_peserta = pk.nomor_peserta and pme.nama_event = e.nama_event and pme.tahun = e.tahun
join match m on m.nama_event = e.nama_event and m.tahun_event = e.tahun
join peserta_mengikuti_match pmm on pmm.nomor_peserta = pk.nomor_peserta and pmm.jenis_babak =  'R16' and pmm.tanggal = m.tanggal and pmm.waktu_mulai = m.waktu_mulai and pmm.status_menang = False and e.tahun = %s and e.nama_event = %s and PPK.jenis_partai = %s;

    """
    cursor.execute(query_nyoba, (tahun_event, nama_event, jenis_partai))

    nyoba_t_5 = cursor.fetchall()



    
    context = {"hasil_pertandingan_header":hasil_pertandingan_header, "FETCH": hasil_pertandingan_header_fetch, "juara_1_ganda":juara_1_ganda, "juara_1_tunggal": juara_1_tunggal, "nyoba":nyoba, "nyoba_2": nyoba_2, "nyoba_3": nyoba_3, "nyoba_4": nyoba_4, "nyoba_5": nyoba_5, "nyoba_t": nyoba_t, "nyoba_t_2": nyoba_t_2, "nyoba_t_3": nyoba_t_3, "nyoba_t_4": nyoba_t_4, "nyoba_t_5": nyoba_t_5 }
    return render(request,'r_hasil_pertandingan.html', context=context)







