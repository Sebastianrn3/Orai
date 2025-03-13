import json
import requests
from django.core.management.base import BaseCommand
from weathers.models import Waterbody
from django.db import models

API_URL = "https://api.meteo.lt/v1/hydro-stations"

class Command(BaseCommand):
    help = "Import waterbodies from JSON file"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching places from API...")

        try:
            response = requests.get(API_URL)
            response.raise_for_status()

            waterbodies = response.json()
            self.stdout.write(f"Received {len(waterbodies)} places.")

            for waterbody in waterbodies:
                Waterbody.objects.update_or_create(
                    code=waterbody["code"],
                    defaults={
                        "name": waterbody.get["name"],
                        "waterbody": waterbody.get("waterBody"),
                        "country_code": waterbody.get["countryCode"],
                        "latitude": waterbody.get["coordinates"]["latitude"],
                        "longitude": waterbody.get["coordinates"]["longitude"],
                    },
                )

            self.stdout.write(self.style.SUCCESS("Places imported successfully!"))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching places: {e}"))