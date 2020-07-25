from django.db import models
from django.db import transaction

from noflys.models import NoFly
from openinghours.models import OpeningHours
from noflys.serializers import NoFlySerializer
from datetime import datetime, timedelta

import re

# Create your models here.

class NoFlyManager(models.Manager):

    @staticmethod
    def ReturnNoFlys(serialize=True):
        """
        Retrieves "nofly" associated with a Project.

        """
        list = NoFly.objects.all()
        if serialize:
            serializer = NoFlySerializer(list, many=True)
            return serializer.data
        else:
            return list

    @staticmethod
    def ReturnNoFlysByLocation(location_id, serialize=True):
        list = NoFly.objects.filter(location = location_id)        
        if serialize:
            serializer = NoFlySerializer(list, many=True)
            return serializer.data
        else:
            return list

    @staticmethod
    def Find(id, serialize=True):
        """
        Retrieves an nofly by its ID. 

        """
        try:
            a = NoFly.objects.get(id=id)
        except:
            return (False, None,)

        if serialize:
            serializer = NoFlySerializer(a)
            nofly = serializer.data
            return (True, nofly,)
        else:
            return (True, a,)
        
    @staticmethod
    def Create(createData):
        """
        Creates an nofly with specified data.

        """
        if 'label' in createData:
            createData['label'] = re.sub('<[^<]+?>', '', createData['label'])
                
        serializer = NoFlySerializer(None, data=createData)
        if serializer.is_valid():
            created = NoFlySerializer(serializer.save())
            return (True, created.data,)
        else:
            return (False, serializer.errors,)
        
    @staticmethod
    def Delete(id):
        """
        Deletes an nofly specified by its ID.

        """
        try:
            a = NoFly.objects.get(id=id)
        except:
            return False
        if a.delete():
            return True
        else:
            return False
        
    @staticmethod
    def Update(id, updateData):
        """
        Updates an nofly with specified data.

        """
        if 'label' in updateData:
            updateData['label'] = re.sub('<[^<]+?>', '', updateData['label'])        
        a = None
        try:
            a = NoFly.objects.get(id=id)
        except Exception as e: print(e)
            
        serializer = NoFlySerializer(a, data=updateData)
        if serializer.is_valid():
            updated = NoFlySerializer(serializer.save())
            return (True, updated.data,)
        else:
            return (False, serializer.errors,)

