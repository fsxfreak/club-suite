from django.db import models
from datetime import datetime

class EventManager(models.Manager):

   #search for upcoming events of a club since today ordered by start time
   #most recent to future
   def get_upcoming_events(self, in_cid):
      upcoming_events=Event.objects.filter(
                        cid=in_cid,
                        end_date__gte=datetime.date.today
                        )
      upcoming_events=upcoming_events.filter(
                        end_time__gte=datetime.datetime.now().time
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

   #did = models.ForeignKey('Division')
   event_name = models.CharField(max_length=100)
   start_date = models.DateField(default=datetime.now)
   start_time = models.TimeField(default='12:00:00')
   end_date = models.DateField(default=datetime.now)
   end_time = models.TimeField(default='12:00:00')
   event_location = models.CharField(max_length=100)
   event_description = models.TextField()
   event_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0)
   accessibility = models.BooleanField(default=True) #True=public, False=private
   required = models.BooleanField(default=False)

   objects = EventManager()

   def __str__(self):
       return self.event_name
