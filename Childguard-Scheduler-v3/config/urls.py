from django.contrib import admin
from django.urls import path, include

handler403 = 'childguard.views.custom_403'
handler404 = 'childguard.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('childguard.urls')),
]
