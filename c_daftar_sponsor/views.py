from django.shortcuts import render

from c_daftar_sponsor.models import Sponsor

# Create your views here.


def show_render(request):
    if request.method == "POST":
        sponsor = request.POST.get("sponsorDropdown")

        # change this onto all sponsor yang atletnya belum daftar
        context = {
            'sponsor_list': Sponsor.objects.all()
        }

        print(sponsor)
        response = render(request, "daftar-sponsor.html", context)
        return response

        # if user is not None:
        # login(request, user)
        # response = HttpResponseRedirect(reverse("cru_tes_kualif_atlet:show_next"))
        # # response.set_cookie("last_login", str(datetime.datetime.now()))
        # return response
        # else:
        #     messages.info(request, "Username atau Password salah!")

    # change this onto all sponsor yang atletnya belum daftar
    sponsor = Sponsor.objects.all()
    # for m in sponsor:
    #     print(m.nama_brand)
    context = {"sponsor_list": sponsor}
    return render(request, "daftar-sponsor.html", context)
