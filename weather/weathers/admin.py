from django.contrib import admin
from .models import City
# Register your models here.

# class CityAdmin(admin.ModelAdmin):
# #     fields = ["name", "country"]

admin.site.register(City)