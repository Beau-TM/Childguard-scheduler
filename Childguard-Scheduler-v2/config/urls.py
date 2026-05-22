"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse

# Deze functie maakt de admin aan via de browser
def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@test.com", "Welkom01!")
        return HttpResponse("Admin aangemaakt!")
    return HttpResponse("Admin bestond al.")

urlpatterns = [
    path('', include('accounts.urls')),
    path('directie/', include('directie.urls', namespace='directie')),
    path('leerkracht/', include('leerkracht.urls', namespace='leerkracht')),
    path('admin/', admin.site.urls),
    path('maak-admin-aan-123/', create_admin),
]