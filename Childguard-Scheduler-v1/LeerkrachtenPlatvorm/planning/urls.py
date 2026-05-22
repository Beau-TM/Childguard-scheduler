from django.urls import path
from . import views

urlpatterns = [
    path('', views.planning_overview, name='planning'),
]