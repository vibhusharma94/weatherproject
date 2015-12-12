# python modules
from datetime import datetime

# rest framework modules
from rest_framework import mixins as rest_mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework import exceptions as res_exceptions
from rest_framework import response as rest_response
from rest_framework import viewsets as rest_viewset
from rest_framework import status as rest_status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication


# app level modules
from apps.apis.weather import utils as weather_utils
from apps.apis.weather import permission as weather_permissions
from apps.apis.weather import serializer as weather_serializer
from apps.apis.weather import models as weather_models


# No need for csrf verification
class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        # Get the underlying HttpRequest object
        request = request._request
        user = getattr(request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        return (user, None)


class StationViewSet(rest_viewset.GenericViewSet):

    queryset = weather_models.WeatherStations.objects.all()
    permission_classes = []
    authentication_classes = (UnsafeSessionAuthentication,)

    # get all available weather stations
    def list(self, request):
        queryset = weather_models.WeatherStations.objects.filter(is_active=True)
        serializer = weather_serializer.WeatherStationSerializer(queryset, many=True)
        res_data = {"stations": serializer.data, "weather_parameters" : weather_utils.weather_parameters}
        return rest_response.Response(res_data)

    # create weather stations
    def create(self, request):
        place = request.data.get("place")
        # get lat and lng from google geocoder api
        location, err = weather_utils.getLatlngFromPlace(place)
        if not location:
            return rest_response.Response(str(err), rest_status=400)
        # calling wunderground api to get station data
        data = weather_utils.fetch_station(location.get("lat"), location.get("lng"))
        try:
            station = weather_models.WeatherStations.objects.get(requesturl=data["requesturl"])
            serializer = weather_serializer.WeatherStationSerializer(instance=station)
        except weather_models.WeatherStations.DoesNotExist:
            serializer = weather_serializer.WeatherStationSerializer(data=data)
            if not serializer.is_valid():
                return rest_response.Response(serializer.errors, status=400)
            serializer.save()
        res_data = {"station": serializer.data}
        return rest_response.Response(res_data, status=rest_status.HTTP_201_CREATED)


    @detail_route(methods=['get'], url_path="plot/graph")
    def plot_graph(self, request, pk=None):
        station = self.get_object()
        # validate all query params. we can do it here this neat way
        serializer = weather_serializer.QueryParamSerializer(data=request.GET)
        if not serializer.is_valid():
            return rest_response.Response(serializer.errors, status=400)
        else:
            start_hour = serializer.validated_data.get("start_hour")
            end_hour = serializer.validated_data.get("end_hour")
            weather_parameter = serializer.validated_data.get("weather_parameter")
            date = request.GET.get("date")
        # fetch weather data by calling wunderground api
        data = weather_utils.fetch_weather_information(station.requesturl, date)
        if data.get("history") and data.get("history").get("observations") and len(data.get("history").get("observations")) > 0:
            observations = data.get("history").get("observations")
            # filter data based on time interval
            data = self.filter_data(observations, weather_parameter, start_hour, end_hour)
            return rest_response.Response(data)
        else:
            return rest_response.Response("No observations available", status=400)

    def filter_data(self, observations, weather_parameter, lower_hour_limit, higher_hour_limit):
        hours = []
        values = []
        for item in observations:
            hour = item.get("utcdate").get("hour")
            d = datetime.strptime(hour, "%H")
            if d >= lower_hour_limit and d <= higher_hour_limit:
                # hour = d.strftime("%I:%M %p")
                # hours.append(hour)
                mins = item.get("utcdate").get("min")
                time = hour + ":" + mins
                hours.append(time)
                if weather_parameter == "temperature":
                    val = item.get("tempm")
                if weather_parameter == "humidity":
                    val = item.get("hum")
                if weather_parameter == "pressure":
                    val = item.get("pressurem")
                values.append(val)
        return dict(hours=hours, values=values, weather_parameter=weather_parameter)
