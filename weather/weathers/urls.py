from django.urls import path
from . import views

app_name = 'weathers'

urlpatterns = [
    path('', views.cities, name='cities'),
    path("<int:pk>", views.detail, name="city"),
    path("add", views.add_city, name="add_city"),
    path("delete/<int:pk>", views.delete_city, name="delete_city"),
    path("summary", views.summary, name="summary"),
]
