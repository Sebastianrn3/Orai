from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

class Place(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    administrative_division = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Waterbody(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    waterbody = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50, default='', blank=True, unique=True)
    country = models.CharField(default='Lietuva', max_length=50)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name} in {self.country}, coordination: {self.latitude}, {self.longitude}'




class CitySlug(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.city.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city.name} ({self.slug})"


class CityWeathers(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.city.name} - {self.temperature}°C, {self.wind_speed} km/h (Updated: {self.updated_at})"