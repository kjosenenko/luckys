
from django.conf.urls import url

from openinghours.views import openingHours as openingHoursEndpoint
from openinghours.views import openingHour as openingHourEndpoint


urlpatterns = [

    url(r'openinghours/$', openingHoursEndpoint),
    url(r'openinghours/(?P<id>\d+)/$', openingHourEndpoint),
]