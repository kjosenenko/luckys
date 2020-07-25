from rest_framework import serializers

from .models import NoFly

class NoFlySerializer(serializers.ModelSerializer):
	class Meta:
		model = NoFly
		fields = ('id', 'name', 'email', 'phone', 'location', 'added')
