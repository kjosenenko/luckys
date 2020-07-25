from django.db import models
from locations.models import Location

class Slot(models.Model):
	name = models.CharField(max_length=128, blank=True, null=True)
	email = models.EmailField(max_length=128, blank=True, null=True)
	phone = models.CharField(max_length=14, blank=True, null=True)
	slot = models.TimeField(auto_now=False, auto_now_add=False)
	open = models.BooleanField(default=True)
	fulfilled = models.BooleanField(default=False)
	nofly = models.BooleanField(default=False)
	location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False)	

	def __str__(self):
		return self.name