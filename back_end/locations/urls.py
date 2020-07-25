
from django.conf.urls import url

from locations.views import locations as locationsEndpoint
from locations.views import location as locationEndpoint


urlpatterns = [

    url(r'locations/$', locationsEndpoint),
    url(r'locations/(?P<id>\d+)/$', locationEndpoint),
]