from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now, timedelta, localtime
from datetime import datetime
import requests

from .models import City, CitySlug, CityWeathers, Place
from .forms import  CityForm
from .helper_functions.weathers import get_weather

API_URL = "https://api.meteo.lt/v1/places/{}/forecasts/long-term"


def cities(request):
    return render(request=request, template_name="weathers/cities.html", context={"cities": City.objects.all()})


def detail(request, slug = None, pk = None):
    if slug:
        city_slug = get_object_or_404(CitySlug, slug=slug)
        city = city_slug.city
    else:
        city = City.objects.get(pk=pk)

    url = f"https://api.meteo.lt/v1/places/{city.name}/forecasts/long-term"
    response = requests.get(url)
    data = response.json()

    temperature, wind_speed = get_weather(latitude = city.latitude,longitude = city.longitude)
    context = {
        "city": city,
        "temperature": temperature,
        "wind_speed": wind_speed,
        "forecasts": data.get("forecastTimestamps", []),
    }
    update_weather(request, pk, temperature = temperature, wind_speed = wind_speed, redirection = False)

    return render(request=request, template_name="weathers/city.html", context=context)


def update_weather(request, pk, temperature = None, wind_speed = None, redirection = True):
    city = get_object_or_404(City, pk=pk)

    if temperature is None or wind_speed is None:
        temperature, wind_speed = get_weather(latitude=city.latitude, longitude=city.longitude)

    CityWeathers.objects.update_or_create(
        city=city,
        defaults={"temperature": temperature, "wind_speed": wind_speed, "updated_at": now()},
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
    return render(request, "weathers/summary.html", {"cities": City.objects.all()})


def get_place_data(request):
    city_name = request.GET.get("name", "").strip()

    try:
        place = Place.objects.get(name__iexact=city_name)
        data = {
            "latitude": place.latitude,
            "longitude": place.longitude,
            "administrative_division": place.administrative_division,
            "country_code": place.country_code,
        }
    except Place.DoesNotExist:
        data = {}

    return JsonResponse(data)


def city_weather(request, city_name="Vildnius"):
    times_of_day = {0: "night", 6: "morning", 12: "afternoon", 18: "evening"}

    def get_weather_data(place_code):
        url = API_URL.format(place_code)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    place = get_object_or_404(Place, name__iexact=city_name)
    forecasts = get_weather_data(place.code).get("forecastTimestamps", [])
    if not forecasts: return render(request, 'weathers/forecast.html', {"error": "Orų nerasta."})

    daily_forecast = {}
    for f in forecasts:
        date, time = f["forecastTimeUtc"].split(" ")
        hour = int(time[:2])

        if date not in daily_forecast: daily_forecast[date] = {}

        if hour in times_of_day:
            daily_forecast[date][times_of_day[hour]] = {
                "temperature": f["airTemperature"],
                "condition": f["conditionCode"],
                "wind_speed": f["windSpeed"],
                "humidity": f["relativeHumidity"],
                "feels_like_temperature":f["feelsLikeTemperature"],
                "time": f["forecastTimeUtc"]
            }
    return render(request, "weathers/forecast.html", {"city": place, "forecasts": daily_forecast})

def footer_context(request):
    return {"current_date": now()}