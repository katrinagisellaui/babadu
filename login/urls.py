from django.urls import path
from login.views import show_render_login, show_render_user_login

app_name = 'login'

urlpatterns = [
    path('', show_render_login, name='login'),
    path('pilih_login', show_render_user_login, name='login'),
]