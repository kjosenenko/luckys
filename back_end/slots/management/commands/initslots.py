from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
import datetime
from locations.models import Location
from openinghours.models import OpeningHours
from slots.models import Slot

class Command(BaseCommand):

    WEEKDAYS = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    help = 'Initialize daily slots for each location in the database'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # Delete all slots in Database
        Slot.objects.all().delete()
        # Get locations
        locations = Location.objects.all()
        for location in locations:
            self.stdout.write(self.style.SUCCESS(location.name))
            now = datetime.datetime.now()
            day = self.WEEKDAYS.index(now.strftime("%A")) + 1
            storeOpeningHours = OpeningHours.objects.filter(location=location, weekday=day)
            slotHour = storeOpeningHours[0].open
            closingHour = storeOpeningHours[0].close
            if storeOpeningHours[0].is_open:
                while slotHour < closingHour:
                    self.stdout.write(self.style.SUCCESS(slotHour))
                    i = 0
                    while i < storeOpeningHours[0].slots:
                        newSlot = Slot.objects.create(location=location, slot=slotHour, open=True, fulfilled=False)
                        i += 1
                    if slotHour.minute == 30:
                        addHour = 1
                        addMinute = -30
                    else:
                        addHour = 0
                        addMinute = 30
                    slotHour = datetime.time(slotHour.hour + addHour, slotHour.minute + addMinute, slotHour.second, slotHour.microsecond)

        # Get opening hours for location
        # Figure out slots for daily hours
        # create slots
#        for poll_id in options['poll_ids']:
#            try:
#                poll = Poll.objects.get(pk=poll_id)
#            except Poll.DoesNotExist:
#                raise CommandError('Poll "%s" does not exist' % poll_id)

#            poll.opened = False
#            poll.save()

#            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
