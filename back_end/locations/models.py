from django.db import models

class Location(models.Model):
  name = models.CharField(max_length=128, blank=False, null=False)
  address = models.CharField(max_length=256, blank=True, null=True)
  phone = models.CharField(max_length=14, blank=False, null=False)
  email = models.EmailField(max_length=128, blank=True, null=True)

  def __str__(self):
    return self.name
