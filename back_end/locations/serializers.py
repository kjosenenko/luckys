
from locations.models import Location
from rest_framework import serializers

# Serializers

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'phone', 'address', 'email',)