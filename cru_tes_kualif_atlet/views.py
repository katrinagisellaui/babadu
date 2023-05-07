from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from cru_tes_kualif_atlet.models import BarangWishlist
# Create your views here.


# def show_render(request):
#     data_barang_wishlist = BarangWishlist.objects.all()
#     context = {
#         'list_barang': data_barang_wishlist,
#         'nama': 'Kak Cinoy'
#     }
#     return render(request, "cru-tes-kualif.html", context)


def show_render(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # user = authenticate(request, username=username, password=password)
        batch = request.POST.get("batchNumber")
        location = request.POST.get("location")
        date = request.POST.get("date")

        context = {
            'batch': batch, 'location': location, 'date': date
        }

        print(batch)
        print(location)
        print(date)
        response = render(request, "cru-tes-kualif-2.html", context)
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
    return render(request, "cru-tes-kualif.html", context)
