from rest_framework import status
from rest_framework.test import APITestCase
from apps.apis.weather import serializer as weather_serializer
from apps.apis.weather import models as weather_models


class CreateStationTest(APITestCase):
    def setUp(self):
        self.data = {'place': 'London, UK'}

    def test_can_create_weather_station(self):
        response = self.client.post("/api/stations/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PlotGraphTest(APITestCase):
    def setUp(self):
        city = "London"
        lat = 51.5
        lng = -0.12
        requesturl = "global/stations/03779.html"
        self.station = weather_models.WeatherStations.objects.create(city=city, lat=lat, lng=lng, requesturl=requesturl)

    def test_can_read_weather_station_list(self):
        url = "/api/stations/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_plot_graph(self):
        url = "http://127.0.0.1:8000/api/stations/1/plot/graph/?start_hour=1:00%20AM&end_hour=1:00%20AM&weather_parameter=temperature&date=20151202"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
