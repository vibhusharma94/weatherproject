from datetime import datetime

from rest_framework import serializers as rest_serializers
from rest_framework import exceptions as rest_exceptions
from apps.apis.weather import models as weather_models


class WeatherStationSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = weather_models.WeatherStations


class QueryParamSerializer(rest_serializers.Serializer):

    date = rest_serializers.CharField(required=False)
    start_hour = rest_serializers.CharField(required=True)
    end_hour = rest_serializers.CharField(required=True)
    weather_parameter = rest_serializers.CharField(required=False)

    def validate(self, value):
        try:
            date = datetime.strptime(value.get("date"), '%Y%m%d').date()
            start_hour = datetime.strptime(value.get('start_hour'), '%I:%M %p')
            end_hour = datetime.strptime(value.get('end_hour'), '%I:%M %p')
            weather_parameter = value.get('weather_parameter')
        except Exception as e:
            raise rest_exceptions.ValidationError(str(e))
        else:
            if start_hour > end_hour:
                raise rest_exceptions.ValidationError("start_hour can't be greather than end_hour")
            if weather_parameter not in ["temperature", "humidity", "pressure"]:
                raise rest_exceptions.ValidationError('Invalid weather parameter')
        return dict(date=date, start_hour=start_hour, end_hour=end_hour, weather_parameter=weather_parameter)