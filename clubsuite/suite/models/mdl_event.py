from django.db import models

from django.utils import timezone

from stdimage.models import StdImageField

class EventManager(models.Manager):

   #search for upcoming events of a club since today ordered by start time
   #most recent to future
   def get_upcoming_events(self, in_cid):
      upcoming_events=Event.objects.filter(
                        cid=in_cid,
                        end_date__gte=timezone.now()
                        ).order_by('start_date', 'start_time')
      return upcoming_events

   #search for all events of a club, ordered from newest to oldest
   def get_all_events(self, in_cid):
      all_events=Event.objects.filter(
                        cid=in_cid
                        ).order_by('-start_date','-start_time')
      return all_events

class Event(models.Model):
   cid = models.ForeignKey(
      'Club',
      on_delete=models.CASCADE
   )

   did = models.ForeignKey('Division', on_delete=models.CASCADE, null=True)
   event_name = models.CharField(max_length=100)
   start_date = models.DateField(default=timezone.now)
   start_time = models.TimeField(default='12:00:00')
   end_date = models.DateField(default=timezone.now)
   end_time = models.TimeField(default='12:00:00')
   event_location = models.CharField(max_length=100)
   event_description = models.TextField()
   event_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0)
   event_fee = models.DecimalField(max_digits=10, decimal_places=2,default=0)
   accessibility = models.BooleanField(default=True) #True=public, False=private
   required = models.BooleanField(default=False)
   image = StdImageField(default="special_event.png",
      variations={'cropped': {'width': 256, 'height': 256, 'crop': True}})

   objects = EventManager()

   def __str__(self):
       return self.event_name
