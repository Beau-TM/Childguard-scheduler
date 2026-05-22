from django.urls import path
from . import views

app_name = 'leerkracht'

urlpatterns = [
    path('dashboard/',             views.dashboard,            name='dashboard'),
    path('gezamenlijke-kalender/', views.gezamenlijke_kalender, name='gezamenlijke_kalender'),
    path('gezamenlijke_kalender/', views.gezamenlijke_kalender, name='gezamenlijke_kalender_alt'),
    path('mijn-lesuren/',          views.mijn_lesuren,          name='mijnlesuren'),
    path('afmeldingen/',           views.afmeldingen,           name='afmeldingen'),
    path('afmelding-indienen/',    views.afmelding_indienen,    name='afmelding_indienen'),
    path('afmelding-annuleren/',   views.afmelding_annuleren,   name='afmelding_annuleren'),
]