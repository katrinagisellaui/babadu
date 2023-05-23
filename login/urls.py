from django.urls import path
from login.views import *

app_name = 'login'

urlpatterns = [
    path('', login_home, name='login_home'),
    path('pilih_login/', login, name='login'),
    path('logout/', logout_user, name='logout_user')
]
