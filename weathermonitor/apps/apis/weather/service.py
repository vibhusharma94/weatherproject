from apps.apis.weather import utils as weather_utils
from apps.apis.weather import permission as weather_permissions
from apps.apis.weather import serializer as weather_serializer
from apps.apis.weather import models as weather_models

latlngpairs = []
latlngpairs.append(dict(lat=51.507351, lng=-0.127758))
latlngpairs.append(dict(lat=40.712784, lng=-74.005941))


def auto_populate_station():
    for location in latlngpairs:
        data = weather_utils.fetch_station(location.get("lat"), location.get("lng"))
        try:
            station = weather_models.WeatherStations.objects.get(requesturl=data["requesturl"])
        except weather_models.WeatherStations.DoesNotExist:
            serializer = weather_serializer.WeatherStationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print serializer.data.get("city") + " station added."
            else:
                print serializer.errors