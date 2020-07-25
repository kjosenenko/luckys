from rest_framework import serializers

from .models import OpeningHours

class OpeningHoursSerializer(serializers.ModelSerializer):
	class Meta:
		model = OpeningHours
		fields = ('id', 'location', 'weekday', 'slots', 'open', 'close', 'is_open')
