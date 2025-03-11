from django.shortcuts import render, redirect, get_object_or_404
from .models import City
from .forms import  CityForm
from .helper_functions.weathers import get_weather

def cities(request):
    cities = City.objects.all()
    context = {"cities": cities}
    return render(request=request, template_name="weathers/cities.html", context=context)

def detail(request, pk):
    city = City.objects.get(pk=pk)
    temperature, wind_speed = get_weather(latitude = city.latitude,longitude = city.longitude)
    context = {
        "city": city,
        # "cities":City.objects.all(),
        "temperature": temperature,
        "wind_speed": wind_speed,
    }
    return render(request=request, template_name="weathers/city.html", context=context)


def add_city(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weathers:cities")
    else:
        form = CityForm()

    return render(request, "weathers/add_city.html", {"form": form})

def delete_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == "POST":
        city.delete()
        return redirect("weathers:cities")
    return render(request=request, template_name="weathers/city_delete_confirm.html", context={"city":city})

def summary(request):
    cities = City.objects.all()
    return render(request, "weathers/summary.html", {"cities": cities})
