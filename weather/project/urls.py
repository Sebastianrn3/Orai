from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path("weathers/", include("weathers.urls")),
    path('admin/', admin.site.urls),
    path('',  home, name='home'),
]