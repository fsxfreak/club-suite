from django.db import models
from datetime import datetime

class Event(models.Model):
   cid = models.ForeignKey(
      'Club',
      on_delete=models.CASCADE
   )
   #did = models.ForeignKey('Division')
   event_name = models.CharField(max_length=100)
   start_time = models.DateTimeField(default=datetime.now, blank=True)
   end_time = models.DateTimeField(default=datetime.now, blank=True)
   event_location = models.CharField(max_length=100)
   event_description = models.CharField(max_length=1000)
   event_cost = models.DecimalField(max_digits=10, decimal_places=2,default=0)
   accessibility = models.BooleanField(default=True) #True=public, False=private
   required = models.BooleanField(default=False)

   def __str__(self):
       return self.event_name
