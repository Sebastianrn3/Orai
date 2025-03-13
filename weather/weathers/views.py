from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
import requests

from unidecode import unidecode

from datetime import datetime, timedelta
from .models import City, CitySlug, CityWeathers, Place
from .forms import  CityForm
from .helper_functions.weathers import get_weather


def cities(request):
    cities = City.objects.all()
    return render(request=request, template_name="weathers/cities.html", context={"cities": cities})


def detail(request, slug = None, pk = None):
    if slug:
        city_slug = get_object_or_404(CitySlug, slug=slug)
        city = city_slug.city
    else:
        city = City.objects.get(pk=pk)

    url = f"https://api.meteo.lt/v1/places/{city.name}/forecasts/long-term"
    response = requests.get(url)
    data = response.json()
    forecasts = data.get("forecastTimestamps", [])

    temperature, wind_speed = get_weather(latitude = city.latitude,longitude = city.longitude)
    context = {
        "city": city,
        "temperature": temperature,
        "wind_speed": wind_speed,
        "forecasts": forecasts,
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
    return render(request, "weathers/summary.html", {"cities": City.objects.all()})


def get_place_data(request):
    city_name = request.GET.get("name", "").strip()
    # normalized_name = unidecode(city_name.lower())
    #
    # print(f"{normalized_name}")

    try:
        place = Place.objects.get(name__iexact=city_name)
        data = {
            "latitude": place.latitude,
            "longitude": place.longitude,
            "administrative_division": place.administrative_division,
            "country_code": place.country_code,
        }
    except Place.DoesNotExist:
        data = {"latitude": None, "longitude": None, "administrative_division": None, "country": None}

    return JsonResponse(data)



def weather_forecast(request):
    url = "https://api.meteo.lt/v1/places/vilnius/forecasts/long-term"
    response = requests.get(url)
    data = response.json()
    forecasts = data.get("forecastTimestamps", [])

    return render(request, "weathers/forecast.html", {"forecasts": forecasts})




API_URL = "https://api.meteo.lt/v1/places/{}/forecasts/long-term"
def get_weather_data(place_code):
    url = API_URL.format(place_code)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def city_weather(request, city_name="Vilnius"):

    place = get_object_or_404(Place, name__iexact=city_name)
    weather_data = get_weather_data(place.code)

    if not weather_data or "forecastTimestamps" not in weather_data:
        return render(request, 'weathers/test.html', {"error": "Oru nerasta."})

    forecasts = weather_data["forecastTimestamps"]

    if not forecasts:
        return render(request, 'weathers/test.html', {"error": "Oru nerasta."})

    current_weather = forecasts[0]

    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

    available_hours = []
    for f in forecasts:
        forecast_time = datetime.strptime(f["forecastTimeUtc"].replace("T", " "), "%Y-%m-%d %H:%M:%S")
        available_hours.append(forecast_time)

    if not available_hours:
        return render(request, 'weathers/test.html', {"error": "Oru nerasta."})

    start_time = min(available_hours, key=lambda t: abs((t - now).total_seconds()))

    hourly_forecast = [
        f for f in forecasts
        if datetime.strptime(f["forecastTimeUtc"].replace("T", " "), "%Y-%m-%d %H:%M:%S") >= start_time
    ]
    hourly_forecast = hourly_forecast[:12:2]

    # ********************
    daily_forecast = {}
    times_of_day = {3: "night", 9: "morning", 15: "afternoon", 21: "evening"}
    print("0")

    for f in forecasts:
        if "forecastTimeUtc" not in f or "airTemperature" not in f:
            print("1")
            continue


        forecast_time = f["forecastTimeUtc"].replace("T", " ")
        date, time = forecast_time.split(" ")
        hour = int(time[:2])

        if date not in daily_forecast:
            daily_forecast[date] = {"night": None, "morning": None, "afternoon": None, "evening": None}
            print("2")

        if hour in times_of_day:

            key = times_of_day[hour]
            # print(f"key:{key}")
            daily_forecast[date][key] = {
                "temperature": f["airTemperature"],
                "condition": f["conditionCode"],
                "wind_speed": f["windSpeed"],
                "humidity": f["relativeHumidity"],
                "time": forecast_time
            }

    weekly_forecast = dict(list(daily_forecast.items())[:8])
    # print(weekly_forecast)
    # print("AAAA",weekly_forecast['2025-03-13']['morning']['temperature'])
    context = {
        "city": place.name,
        "current_weather": current_weather,
        "hourly_forecast": hourly_forecast,
        "weekly_forecast": weekly_forecast,
    }
    return render(request, "weathers/test.html", context)