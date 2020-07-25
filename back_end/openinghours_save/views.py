from rest_framework import viewsets
from .serializers import OpeningHoursSerializer
from .models import OpeningHours

class OpeningHoursViewSet(viewsets.ModelViewSet):
	queryset = OpeningHours.objects.all().order_by('weekday')
	serializer_class = OpeningHoursSerializer
