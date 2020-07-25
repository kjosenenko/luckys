from django.db import models
from locations.models import Location

class NoFly(models.Model):
	name = models.CharField(max_length=128, blank=True, null=True)
	email = models.EmailField(max_length=128, blank=True, null=True)
	phone = models.CharField(max_length=14, blank=True, null=True)
	location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False)
	added = models.DateTimeField(auto_now_add=True, blank=True)	

	def __str__(self):
		return self.name