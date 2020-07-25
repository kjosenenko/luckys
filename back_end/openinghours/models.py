from django.db import models
from locations.models import Location 

WEEKDAYS = [
	(1, "Sunday"),
	(2, "Monday"),
	(3, "Tuesday"),
	(4, "Wednesday"),
	(5, "Thursday"),
	(6, "Friday"),
	(7, "Saturday"),
]

class OpeningHours(models.Model):
	
	ordering = ['location', 'weekday', 'from_hour']

	location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False)	
	weekday = models.IntegerField(choices=WEEKDAYS)
	slots = models.IntegerField(blank=False, null=True)
	open = models.TimeField(blank=True, null=True)
	close = models.TimeField(blank=True, null=True)
	is_open = models.BooleanField(default=True)
