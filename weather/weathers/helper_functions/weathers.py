from django.contrib.sites import requests
import requests

# latitude = 54.68
# longitude = 25.27

def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    data = requests.get(url=url)

    temperature = data.json()["current"]["temperature_2m"]
    print(f"{temperature}°C")

    wind_speed = data.json()["current"]["wind_speed_10m"]
    print(f"{wind_speed}km/h")

    return temperature, wind_speed