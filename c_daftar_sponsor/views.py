from django.shortcuts import render

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
    return render(request, "daftar-sponsor.html", context)
