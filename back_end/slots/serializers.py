from rest_framework import serializers

from .models import Slot

class SlotSerializer(serializers.ModelSerializer):
	class Meta:
		model = Slot
		fields = ('id', 'name', 'email', 'phone', 'slot', 'open', 'fulfilled', 'nofly', 'location')
