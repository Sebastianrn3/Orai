from django.urls import path
from . import views

app_name = 'weathers'

urlpatterns = [
    path('', views.cities, name='cities'),
    path('forecast/<str:city_name>/', views.city_weather, name='forecast'),
    path("add", views.add_city, name="add_city"),
    path("edit/<int:pk>", views.edit_city, name="edit_city"),
    path("delete/<int:pk>", views.delete_city, name="delete_city"),
    path("summary", views.summary, name="summary"),
    path("update_weather/<int:pk>/", views.update_weather, name="update_weather"),
    path("get_place_data/", views.get_place_data, name="get_place_data"),
    path("<int:pk>", views.detail, name="city_by_id"),

    # path("<slug:slug>/", views.detail, name="city"),
]
