from django.db import models
from django.db import transaction

from slots.models import Slot
from openinghours.models import OpeningHours
from slots.serializers import SlotSerializer
from datetime import datetime, timedelta

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import re

# Create your models here.

class SlotManager(models.Manager):

    @staticmethod
    def SendVerificationEmail(name, email, phone, slot, location):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = # Enter your address
        receiver_email = # Enter receiver address
        password = # Enter password for sender_email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Reservation for: " + str(name)
        message["From"] = sender_email
        message["To"] = receiver_email
        # Create the plain-text and HTML version of your message
        
        text = """\
        New Reservation generated for:
        Name: """ + name + """"
        Email: """ + email + """"
        Phone: """ + str(phone) + """"
        Slot: """ + SlotManager.timeConvert(slot) + """
        Location: """ + location.name
        
        html = """\
        <html>
          <body>
            <p><h4>Reservation created for:</h4> <br \>
               <b>Name:</b> """ + name + """<br>
               <b>Email:</b> """ + email + """<br>
               <b>Phone:</b> """ + str(phone) + """<br>
               <b>Slot:</b> """ + SlotManager.timeConvert(slot) + """<br>               
               <b>Location:</b> """ + location.name + """<br>  
            </p>
          </body>
        </html>
        """       
    
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    @staticmethod
    def timeConvert(slot):
        time = repr(slot)
        hour = (time[1:3])
        minutes = (time[3:6])
        if int(hour) > 12:
            hour = int(hour) - 12
        standardTime = str(hour) + str(minutes)
        return standardTime

    @staticmethod
    def ReturnSlots(serialize=True):
        """
        Retrieves "slot" associated with a Project.

        """
        list = Slot.objects.all()
        if serialize:
            serializer = SlotSerializer(list, many=True)
            return serializer.data
        else:
            return list

    @staticmethod
    def ReturnSlotsOpen(serialize=True):
        list = Slot.objects.filter(open = True).order_by('slot', 'location')        
        if serialize:
            serializer = SlotSerializer(list, many=True)
            allOpenSlots = serializer.data
            uniqueOpenSlots = []
            for slot in allOpenSlots:
                add = True
                for uniqueSlot in uniqueOpenSlots:
                    if uniqueSlot['location'] == slot['location'] and uniqueSlot['slot'] == slot['slot']:
                        add = False
                one_hour_ago = datetime.now() + timedelta(hours=-1)
                if one_hour_ago.strftime("%H:%M:%S") > slot['slot']:
                    add = False
                if add:
                    uniqueOpenSlots.append(slot)
            return uniqueOpenSlots
        else:
            return list

    @staticmethod
    def ReturnSlotsByLocation(location_id, serialize=True):
        list = Slot.objects.filter(location = location_id)        
        if serialize:
            serializer = SlotSerializer(list, many=True)
            slots = serializer.data
            current_slots = []
            for slot in slots:
                one_hour_ago = datetime.now() + timedelta(hours=-1)
                if one_hour_ago.strftime("%H:%M:%S") < slot['slot']:
                    current_slots.append(slot)
            return current_slots
        else:
            return list



    @staticmethod
    def Find(id, serialize=True):
        """
        Retrieves an slot by its ID. 

        """
        try:
            a = Slot.objects.get(id=id)
        except:
            return (False, None,)

        if serialize:
            serializer = SlotSerializer(a)
            slot = serializer.data
            return (True, slot,)
        else:
            return (True, a,)
        
    @staticmethod
    def Create(createData):
        """
        Creates an slot with specified data.

        """
        if 'label' in createData:
            createData['label'] = re.sub('<[^<]+?>', '', createData['label'])
                
        serializer = SlotSerializer(None, data=createData)
        if serializer.is_valid():
            created = SlotSerializer(serializer.save())
            return (True, created.data,)
        else:
            return (False, serializer.errors,)
        
    @staticmethod
    def Delete(id):
        """
        Deletes an slot specified by its ID.

        """
        try:
            a = Slot.objects.get(id=id)
        except:
            return False
        if not a.open:
            return False
        if a.delete():
            return True
        else:
            return False
        
    @staticmethod
    def Update(id, updateData):
        """
        Updates an slot with specified data.

        """

        if 'label' in updateData:
            updateData['label'] = re.sub('<[^<]+?>', '', updateData['label'])        
        a = None
        try:
            a = Slot.objects.get(id=id)
        except Exception as e: print(e)

        if a.nofly or a.fulfilled:
            if a.name != updateData['name'] or a.email != updateData['email'] or a.phone != updateData['phone']:
                return (False, {"status": "This slot is already taken."})
            serializer = SlotSerializer(a, data=updateData)
            if serializer.is_valid():
                updated = SlotSerializer(serializer.save())
                return (True, updated.data,)
            else:
                return (False, serializer.errors,)

        if updateData['nofly'] or updateData['fulfilled']:
            serializer = SlotSerializer(a, data=updateData)
            if serializer.is_valid():
                updated = SlotSerializer(serializer.save())
                return (True, updated.data,)
            else:
                return (False, serializer.errors,)
        
        if not a.open:
            if not updateData['open']:
                return (False, {"status": "This slot is already taken."})

        serializer = SlotSerializer(a, data=updateData)
        if serializer.is_valid():
            updated = SlotSerializer(serializer.save())
            if not updateData['open']:
                SlotManager.SendVerificationEmail(updateData['name'], updateData['email'], updateData['phone'], updateData['slot'], a.location)
            return (True, updated.data,)
        else:
            return (False, serializer.errors,)

