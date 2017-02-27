from django.db import models

class EventManager(models.Manager):

   #search for upcoming events of a club since today ordered by start time
   def get_upcoming_events(in_cid):
      upcoming_events=Event.objects.filter(
                        cid=in_cid,
                        end_time__gte=datetime.date.today()
                        ).order_by('start_time')
      return upcoming_events

class Event(models.Model):
   cid = models.ForeignKey(
      'Club',
      on_delete=models.CASCADE
   )
   did = models.ForeignKey('Division')
   event_name = models.CharField(max_length=100,unique=True)
   start_time = models.DateTimeField()
   end_time = models.DateTimeField()
   event_location = models.CharField(max_length=100)
   event_description = models.CharField(max_length=1000)
   event_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0)
   accessibility = models.BooleanField(default=True) #True=public, False=private
   required = models.BooleanField(default=False)

   objects = EventManager()

   def __str__(self):
       return self.event_name
