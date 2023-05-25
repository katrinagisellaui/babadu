from datetime import datetime

import psycopg2
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def show_render(request):
    user_name = request.COOKIES.get("nama")
    user_id = request.COOKIES.get("id")
    user_email = request.COOKIES.get("email")
    user_role = request.COOKIES.get("role")
    print(user_name, user_email, user_id, user_role)

    context = {
        "username": user_name,
        "id": user_id,
        "email": user_email,
        "role": user_role,
        "dummyrole": "UMPIRE",
    }
    return render(request, "tes-kualif-home.html", context)


def show_create_ujian(request):
    context = {
    }
    return render(request, "form-create-ujian.html", context)


def create_ujian(request):
    if request.method == "POST":
        tahun = request.POST.get("tahun")
        batch = request.POST.get("batch")
        location = request.POST.get("tempat")
        date = request.POST.get("tanggal")

        connection = None
        cursor = None
        try:
            connection = connect_db()
            cursor = connection.cursor()

            insert_query = "INSERT INTO UJIAN_KUALIFIKASI (Tahun, Batch, Tempat, Tanggal) VALUES (%s, %s, %s, %s)"
            values = (tahun, batch, location, date)

            cursor.execute(insert_query, values)
            connection.commit()

            print("Data inserted successfully.")

            response_data = {'status': 'success'}
            # Mengembalikan response sebagai JSON
            return JsonResponse(response_data)

        except psycopg2.Error as e:
            print("Error inserting data:", e)
            response_data = {'status': 'error', 'message': str(e)}
            # Mengembalikan response sebagai JSON
            return JsonResponse(response_data)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")

    else:
        response_data = {'status': 'error', 'message': 'Invalid request method'}
        # Mengembalikan response sebagai JSON
        return JsonResponse(response_data)


def list_ujian(request):
    # get list ujian dari db
    role = request.COOKIES.get("role")
    connection = None
    cursor = None
    fetched_data = None
    try:
        connection = connect_db()
        cursor = connection.cursor()

        query = "SELECT * FROM UJIAN_KUALIFIKASI"

        cursor.execute(query)
        connection.commit()

        fetched_data = cursor.fetchall()

        print(fetched_data)
        print("Data query success.")

        context = {
            'data': fetched_data,
            'role': role,
        }
        # Mengembalikan response sebagai JSON
        return render(request, "list-ujian-kualif.html", context)

    except psycopg2.Error as e:
        print("Error querying data:", e)
        response_data = {'status': 'error', 'message': str(e)}
        # Mengembalikan response sebagai JSON
        return JsonResponse(response_data)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")


def ujian_atlet(request):
    tahun = request.GET.get("tahun")
    batch = request.GET.get("batch")
    location = request.GET.get("tempat")
    date = request.GET.get("tanggal")

    ujian_data = {
        "tahun": tahun,
        "batch": batch,
        "tempat": location,
        "tanggal": date,
    }

    context = {
        "ujian_data": ujian_data,
        "pertanyaan": create_pertanyaan(),
    }
    # Mengembalikan response sebagai JSON
    return render(request, "ujian-kualifikasi-soal.html", context)


def submit_ujian(request):
    if request.method == "POST":
        user_id = request.COOKIES.get("id")

        answer1 = request.POST.get("1")
        answer2 = request.POST.get("2")
        answer3 = request.POST.get("3")
        answer4 = request.POST.get("4")
        answer5 = request.POST.get("5")
        question = create_pertanyaan()

        jawaban_benar = 0
        i = 0
        for answer in [answer1, answer2, answer3, answer4, answer5]:
            if question[i].get("jawaban") == answer:
                jawaban_benar += 1
            i += 1
        is_lulus = "TRUE" if jawaban_benar >= 4 else "FALSE"
        print(jawaban_benar)

        tahun = request.POST.get("tahun")
        batch = request.POST.get("batch")
        tempat = request.POST.get("tempat")
        date = request.POST.get("tanggal")
        date = datetime.strptime(date, '%m %d, %y').date()

        connection = None
        cursor = None
        try:
            connection = connect_db()
            cursor = connection.cursor()

            query = "INSERT INTO ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI (ID_Atlet, Tahun, Batch, Tempat, Tanggal, Hasil_Lulus) VALUES" \
                    "(%s, %d, %d, %s, %s, %s)".format(
                user_id, tahun, batch, tempat, date, is_lulus
            )

            cursor.execute(query)
            connection.commit()

            print("Data insert query success.")

            # TODO: redirect ke riwayat ujian kualif
            return render(request, "riwayat-ujian-kualif.html")

        except psycopg2.Error as e:
            print("Error querying data:", e)
            response_data = {'status': 'error', 'message': str(e)}
            # Mengembalikan response sebagai JSON
            return JsonResponse(response_data)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")


def riwayat_ujian(request):
    user_id = request.COOKIES.get("id")
    user_role = request.COOKIES.get("role")

    connection = None
    cursor = None
    query = None
    try:
        connection = connect_db()
        cursor = connection.cursor()

        if user_role == "ATLET":
            query = "SELECT * FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI ANUK WHERE ANUK.ID_Atlet = '{}'".format(user_id)
        else:
            query = "SELECT M.nama, ANUK.tahun, ANUK.batch, ANUK.tempat, ANUK.tanggal, ANUK.hasil_lulus " \
                    "FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI ANUK " \
                    "JOIN MEMBER M ON ANUK.ID_Atlet = M.id"

        cursor.execute(query)
        connection.commit()

        fetched_data = cursor.fetchall()

        print(fetched_data)
        print("Data insert query success.")

        context = {
            "riwayat": fetched_data,
            "role": user_role,
        }

        return render(request, "riwayat-ujian-kualif.html", context)

    except psycopg2.Error as e:
        print("Error querying data:", e)
        response_data = {'status': 'error', 'message': str(e)}
        # Mengembalikan response sebagai JSON
        return JsonResponse(response_data)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")
    context = {

    }
    return render(request, "list-ujian-kualif.html")


def create_pertanyaan():
    list_pertanyaan = [
        {"pertanyaan": "Pukulan overhead yang meluncur dekat net dan jatuh di depan lapangan lawan disebut...",
         "option": ["Servis", "Dropshot", "Netting"],
         "jawaban": "Netting",
         },
        {"pertanyaan": "Underhand disebut pula...",
         "option": ["Pukulan dari bawah", "Pukulan dari samping", "Pukulan lob"],
         "jawaban": "Pukulan dari bawah",
         },
        {"pertanyaan": "Servis dengan pukulan melambung tinggi ke belakang disebut...",
         "option": ["Drive service", "Flick service", "Lob service"],
         "jawaban": "Lob service",
         },
        {"pertanyaan": "Pukulan yang dilakukan seperti smash disebut...",
         "option": ["Netting", "Clear", "Dropshot"],
         "jawaban": "Dropshot",
         },
        {"pertanyaan": "Pukulan sevis yang sering digunakan oleh pemain tunggal adalah...",
         "option": ["Short service", "Medium service", "Long service"],
         "jawaban": "Short service",
         },
    ]

    return list_pertanyaan


def connect_db():
    return psycopg2.connect(
        user="postgres",
        password="uerDeirCf7NJNyoYqW5Q",
        host="containers-us-west-128.railway.app",
        port="6881",
        database="railway",
    )
