"""project_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('athlete-qualification/', include('cru_tes_kualif_atlet.urls')),
    path('athlete-registration/', include('cr_daftar_atlet.urls')),
    path('sponsor-registration/', include('c_daftar_sponsor.urls')),
    path('r_list_event/', include('r_list_event.urls')),
    path('cru_daftar_event/', include('cru_daftar_event.urls')),
    path('rd_enrolled_event/', include('rd_enrolled_event.urls',
         namespace='rd_enrolled_event')),
    path('', include('login.urls', namespace='login')),
    path('dashboard/', include('dashboard.urls')),
    path('pengguna/', include('cru_pengguna.urls', namespace='cru_pengguna')),
    path('r_enrolled_partai/', include('r_enrolled_partai_kompetisi_event.urls',
         namespace='r_enrolled_partai_kompetisi_event')),

]
