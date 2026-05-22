from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',               views.login_view,        name='login'),
    path('logout/',        views.logout_view,        name='logout'),
    path('set-password/',  views.set_password_view,  name='set_password'),
]
