from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class WeatherStations(models.Model):
    city = models.CharField(null=False, max_length=255, blank=False)
    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)
    requesturl = models.CharField(null=False, max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created'

    def __unicode__(self):
        return self.city
