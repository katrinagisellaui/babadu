from django.urls import path
from r_list_event.views import *

app_name = 'r_list_event'

urlpatterns = [
    path('', get_partai_kompetisi, name='get_partai_kompetisi'),
    path('lihat-hasil/<str:nama_event>/<int:tahun_event>/<str:jenis_partai>/', lihat_hasil, name='lihat_hasil'),


]
