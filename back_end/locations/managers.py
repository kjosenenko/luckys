from django.db import models
from django.db import transaction

from locations.models import Location
from openinghours.models import OpeningHours
from locations.serializers import LocationSerializer
from openinghours.serializers import OpeningHoursSerializer

import re

# Create your models here.

class LocationManager(models.Manager):

    @staticmethod
    def ReturnLocations(serialize=True):
        """
        Retrieves "location" associated with a Project.

        """
        list = Location.objects.all()
        if serialize:
            serializer = LocationSerializer(list, many=True)
            return serializer.data
        else:
            return list

    @staticmethod
    def Find(id, serialize=True):
        """
        Retrieves an location by its ID. 

        """
        try:
            a = Location.objects.get(id=id)
            b = OpeningHours.objects.filter(location=a)     
        except:
            return (False, None,)

        if serialize:
            serializer = LocationSerializer(a)
            location = serializer.data
            location_hours = []
            for openinghour in b:
                this_hour = OpeningHoursSerializer(openinghour)
                location_hours.append(this_hour.data)
            location['opening_hours'] = location_hours
            return (True, location,)
        else:
            return (True, a,)
        
    @staticmethod
    def Create(createData):
        """
        Creates an location with specified data.

        """
        if 'label' in createData:
            createData['label'] = re.sub('<[^<]+?>', '', createData['label'])
                
        serializer = LocationSerializer(None, data=createData)
        if serializer.is_valid():
            created = LocationSerializer(serializer.save())
            return (True, created.data,)
        else:
            return (False, serializer.errors,)
        
    @staticmethod
    def Delete(id):
        """
        Deletes an location specified by its ID.

        """
        try:
            a = Location.objects.get(id=id)
        except:
            return False
        if a.delete():
            return True
        else:
            return False
        
    @staticmethod
    def Update(id, updateData):
        """
        Updates an location with specified data.

        """
        try:
            a = Location.objects.get(id=id)
        except:
            return (False, None,)            
        serializer = LocationSerializer(a, data=updateData)
        if serializer.is_valid():
            updated = LocationSerializer(serializer.save())
            return (True, updated.data,)
        else:
            return (False, serializer.errors,)

