from django.shortcuts import render, redirect, get_object_or_404
from .models import City, CitySlug, CityWeathers
from .forms import  CityForm
from .helper_functions.weathers import get_weather
from django.http import HttpResponse
from django.utils.timezone import now

def cities(request):
    cities = City.objects.all()
    return render(request=request, template_name="weathers/cities.html", context={"cities": cities})

def detail(request, slug = None, pk = None):
    if slug:
        city_slug = get_object_or_404(CitySlug, slug=slug)
        city = city_slug.city
    else:
        city = City.objects.get(pk=pk)

    temperature, wind_speed = get_weather(latitude = city.latitude,longitude = city.longitude)
    context = {
        "city": city,
        "temperature": temperature,
        "wind_speed": wind_speed,
    }

    update_weather(request, pk, temperature = temperature, wind_speed = wind_speed, redirection = False)
    return render(request=request, template_name="weathers/city.html", context=context)

def update_weather(request, pk, temperature = None, wind_speed = None, redirection = True):
    city = get_object_or_404(City, pk=pk)

    if not temperature or not wind_speed:
        temperature, wind_speed = get_weather(latitude=city.latitude, longitude=city.longitude)

    weather_record, created = CityWeathers.objects.update_or_create(
        city=city,
        defaults={
            "temperature": temperature,
            "wind_speed": wind_speed,
            "updated_at": now(),
        },
    )
    if redirection:
        return redirect("weathers:summary")



def add_city(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weathers:cities")
    else:
        form = CityForm()

    return render(request, "weathers/add_city.html", {"form": form})

def edit_city(request, pk):
    city = get_object_or_404(City, pk=pk)

    if request.method == "POST":
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect("weathers:summary")
    else:
        form = CityForm(instance=city)

    return render(request, "weathers/edit_city.html", {"form": form, "city": city})

def delete_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    if request.method == "POST":
        city.delete()
        return redirect("weathers:cities")
    return render(request=request, template_name="weathers/city_delete_confirm.html", context={"city":city})

def summary(request):
    cities = City.objects.all()
    return render(request, "weathers/summary.html", {"cities": cities})