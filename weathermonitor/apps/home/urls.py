
from django.conf.urls import patterns, include


urlpatterns = patterns(
    '',
    (r'^$', 'apps.home.views.index'),
)