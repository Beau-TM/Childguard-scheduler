# urls.py  (voeg toe aan je app of project urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('',            views.login_view,       name='login'),
    path('logout/',     views.logout_view,       name='logout'),
    path('set-password/', views.set_password_view, name='set_password'),
    path('reset-demo/', views.reset_demo_view,   name='reset_demo'),

    # Voeg hier later jouw andere pagina's toe:
    # path('dashboard/', views.dashboard_view, name='dashboard'),
]
