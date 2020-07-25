from django.db import models
from django.db import transaction
from openinghours.models import OpeningHours
from openinghours.serializers import OpeningHoursSerializer
from datetime import datetime, timedelta

import re

# Create your models here.

class OpeningHourManager(models.Manager):

    @staticmethod
    def ReturnOpeningHours(serialize=True):
        """
        Retrieves "openingHour" associated with a Project.

        """
        list = OpeningHours.objects.all()
        if serialize:
            serializer = OpeningHoursSerializer(list, many=True)
            return serializer.data
        else:
            return list

    @staticmethod
    def Find(id, serialize=True):
        """
        Retrieves an openingHour by its ID. 

        """
        try:
            a = OpeningHours.objects.get(id=id)
        except:
            return (False, None,)

        if serialize:
            serializer = OpeningHoursSerializer(a)
            openingHour = serializer.data
            return (True, openingHour,)
        else:
            return (True, a,)
        
    @staticmethod
    def Create(createData):
        """
        Creates an openingHour with specified data.

        """
        if 'label' in createData:
            createData['label'] = re.sub('<[^<]+?>', '', createData['label'])
                
        serializer = OpeningHoursSerializer(None, data=createData)
        if serializer.is_valid():
            created = OpeningHoursSerializer(serializer.save())
            return (True, created.data,)
        else:
            return (False, serializer.errors,)
        
    @staticmethod
    def Delete(id):
        """
        Deletes an openingHour specified by its ID.

        """
        try:
            a = OpeningHours.objects.get(id=id)
        except:
            return False
        if a.delete():
            return True
        else:
            return False
        
    @staticmethod
    def Update(id, updateData):
        """
        Updates an openingHour with specified data.

        """
        if 'label' in updateData:
            updateData['label'] = re.sub('<[^<]+?>', '', updateData['label'])        
        a = None
        try:
            a = OpeningHours.objects.get(id=id)
        except Exception as e: print(e)
            
        serializer = OpeningHoursSerializer(a, data=updateData)
        if serializer.is_valid():
            updated = OpeningHoursSerializer(serializer.save())
            return (True, updated.data,)
        else:
            return (False, serializer.errors,)

