from django.conf.urls import patterns, include
from rest_framework import routers
from apps.apis.weather import views as weather_views

router = routers.SimpleRouter()
router.register(r'stations', weather_views.StationViewSet)

urlpatterns = patterns(
    '',
    (r'^', include(router.urls)),
)
