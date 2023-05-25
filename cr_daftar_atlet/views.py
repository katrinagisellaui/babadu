from django.db import connection
from django.shortcuts import render, redirect
from cr_daftar_atlet.models import *
# Create your views here.


def show_render(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # user = authenticate(request, username=username, password=password)
        atlet = request.POST.get("athleteDropdown")

        context = {
            'batch': atlet
        }

        print(atlet)
        response = render(request, "list-atlet.html", context)
        # response.set_cookie("last_login", str(datetime.datetime.now()))
        return response

        # if user is not None:
        # login(request, user)
        # response = HttpResponseRedirect(reverse("cru_tes_kualif_atlet:show_next"))
        # # response.set_cookie("last_login", str(datetime.datetime.now()))
        # return response
        # else:
        #     messages.info(request, "Username atau Password salah!")
    
    context = {}
    return render(request, "cr-daftar-atlet.html", context)


def display_atlet(request):
    if "username" not in request.session:
        return redirect('/login')
    response={}
    response['atlet_terkualifikasi'] = get_atlet_kualif()
    return render(request, 'list-atlet.html', response)

def get_atlet_kualif():
    query= """
    SELECT m.nama, a.tgl_lahir, a.negara_asal, a.play_right, 
    a.height, a.world_rank, ak.world_tour_rank, a.jenis_kelamin
    from member m
    join atlet a on a.id = m.id
    join atlet_terkualifikasi ak on a.id = m.id;
    """


def get_atlet_kualifikasi(request):
    
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
    

    atlet_non_kualif = AtletNonKualif.objects.all()
    cursor = connection.cursor()
    cursor.execute("SELECT distinct m.nama, a.tgl_lahir, a.negara_asal, a.play_right,\
                    a.height, a.world_rank, a.jenis_kelamin, p.total_point\
                    from member m\
                    join atlet a on a.id = m.id\
                    join atlet_non_kualifikasi an on an.id_atlet = m.id\
                    join point_history  p on p.id_atlet = m.id;")  # add where sponsor user login
    atlet_non_kualif = cursor.fetchall()

    atlet_ganda = AtletGanda.objects.all()
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

# bagian untuk CR daftar atlet

def c_latih_atlet(request):
    if request.method == "POST":
        id_atlet = request.POST.get("athleteDropdown")
        myid = request.COOKIES.get('id')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ATLET_PELATIH\
                        (id_pelatih, id_atlet)\
                        VALUES ('{}','{}')".format(myid, id_atlet)\
                        )
        return redirect("cr_daftar_atlet:r_latih_atlet")

    # if (request.COOKIES.get('id') == None):
    #     return redirect("dashboard:show_forbidden")

    myid = request.COOKIES.get('id')
    cursor = connection.cursor()
    cursor.execute("SELECT m.id, m.nama FROM MEMBER m, atlet a\
                   WHERE m.id NOT IN (\
                   SELECT id_atlet\
                   FROM atlet_pelatih\
                   WHERE id_pelatih = '{}') and m.id = a.id;".format(myid))
    blm_dilatih_list = cursor.fetchall()

    context = {"blm_dilatih": blm_dilatih_list}
    return render(request, "cr-daftar-atlet.html", context)

def r_latih_atlet(request):
    # if (request.COOKIES.get('id') == None):
    #     return redirect("dashboard:show_forbidden")

    print(request.COOKIES.get('nama'))
    print(request.COOKIES.get('email'))
    print(request.COOKIES.get('id'))

    myid = request.COOKIES.get('id')
    nama = request.COOKIES.get('nama')
    email = request.COOKIES.get('email')

    # if (myid == None or nama == None or email == None):
    #     return render(request, "forbidden.html")
    
    cursor = connection.cursor()
    # cursor.execute("SELECT nama_brand, tgl_mulai, tgl_selesai \
    #                FROM sponsor, atlet_sponsor\
    #                WHERE id_sponsor = id\
    #                AND id_atlet = '{}'".format(myid))
    cursor.execute("select m.nama, m.email, a.world_rank from member m, atlet a, atlet_pelatih ap\
                    where m.id = a.id AND m.id = ap.id_atlet and ap.id_pelatih = '{}'".format(myid))
    atlet_dilatih = cursor.fetchall()

    context = {"atlet_dilatih": atlet_dilatih}
    return render(request, "list-atlet-dilatih.html", context)








