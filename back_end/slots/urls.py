
from django.conf.urls import url

from slots.views import slots as slotsEndpoint
from slots.views import slot as slotEndpoint
from slots.views import slotByLocation as slotLocationEndpoint
from slots.views import slotsOpen as slotsOpenEndpoint


urlpatterns = [

    url(r'slots/$', slotsEndpoint),
    url(r'slots/(?P<id>\d+)/$', slotEndpoint),
    url(r'slots/location/(?P<location_id>\d+)/$', slotLocationEndpoint),
    url(r'slots/open/$', slotsOpenEndpoint),
]