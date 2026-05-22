from django.urls import path
from . import views

app_name = 'directie'

urlpatterns = [
    path('dashboard/',          views.dashboard,          name='dashboard'),
    path('kalender/',           views.kalender,           name='kalender'),
    path('planning-genereren/', views.planning_genereren, name='planning_genereren'),
    path('speciale-dagen/',     views.speciale_dagen,     name='speciale_dagen'),
    path('afmeldingen/',        views.afmeldingen,        name='afmeldingen'),
    path('afmeldingen/<int:afmelding_id>/verwerk/', views.verwerk_afmelding, name='verwerk_afmelding'),
    path('leerkrachten/',       views.leerkrachten,       name='leerkrachten'),
    path('school-overzicht/',   views.school_overzicht,   name='school_overzicht'),
    path('planning-geschiedenis/', views.planning_geschiedenis, name='planning_geschiedenis'),
    path('planning-geschiedenis/<int:planning_id>/', views.planning_detail, name='planning_detail'),
]
