import googlemaps
import requests
from django.conf import settings


def getLatlngFromPlace(place):
    try:
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        geocode_result = gmaps.geocode(place)
        location = geocode_result[0].get("geometry").get("location")
        return location, None
    except Exception as e:
        return None, e


def fetch_station(lat, lng):
    url = settings.WEATHER_API_URL + settings.WEATHER_API_KEY + "/geolookup/q/" + str(lat) + "," + str(lng) + ".json"
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        return None
    if r.status_code == 200:
        data = r.json()
        city = data.get("location").get("city")
        lat = data.get("location").get("lat")
        lng = data.get("location").get("lon")
        requesturl = data.get("location").get("requesturl")
        if not all([city, lat, lng, requesturl]):
            return None
        return dict(city=city, lat=lat, lng=lng, requesturl=requesturl)
    else:
        return None


def fetch_weather_information(requesturl, date):
    url = settings.WEATHER_API_URL + settings.WEATHER_API_KEY + "/history_" + date + "/q/" + requesturl.split(".")[0]+ ".json"
    print url
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        return None
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        return None


weather_parameters = []
weather_parameters.append(dict(name="temperature", id=1))
weather_parameters.append(dict(name="humidity", id=2))
weather_parameters.append(dict(name="pressure", id=3))
