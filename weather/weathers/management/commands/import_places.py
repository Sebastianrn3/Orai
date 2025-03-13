import json
import requests
from django.core.management.base import BaseCommand
from weathers.models import Place
from django.db import models

#2495 vietovių:
API_URL = "https://api.meteo.lt/v1/places"

class Command(BaseCommand):
    help = "Import places from JSON file"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching places from API...")

        try:
            response = requests.get(API_URL)
            response.raise_for_status()

            places = response.json()
            self.stdout.write(f"Received {len(places)} places.")

            for place in places:
                Place.objects.update_or_create(
                    code=place["code"],
                    defaults={
                        "name": place["name"],
                        "administrative_division": place.get("administrativeDivision"),
                        "country_code": place["countryCode"],
                        "latitude": place["coordinates"]["latitude"],
                        "longitude": place["coordinates"]["longitude"],
                    },
                )

            self.stdout.write(self.style.SUCCESS("Places imported successfully!"))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching places: {e}"))