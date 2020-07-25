
from django.conf.urls import url

from noflys.views import noflys as noflysEndpoint
from noflys.views import nofly as noflyEndpoint
from noflys.views import noflyByLocation as noflyLocationEndpoint


urlpatterns = [

    url(r'noflys/$', noflysEndpoint),
    url(r'noflys/(?P<id>\d+)/$', noflyEndpoint),
    url(r'noflys/location/(?P<location_id>\d+)/$', noflyLocationEndpoint),
]