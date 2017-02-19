from django.db import models

class Club(models.Model):
   club_name = models.CharField(max_length=50)

   C_CHOICES = (
       ('PUB','Public'),
       ('PRI','Private')
   )
   club_type = models.CharField(max_length=3,choices=C_CHOICES,default='PUB')
   club_description = models.CharField(max_length=1000)
