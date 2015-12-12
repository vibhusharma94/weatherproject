from django.contrib import admin
from apps.apis.weather import models as weather_models

admin.site.register(weather_models.WeatherStations)
