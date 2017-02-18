from django.db import models

class Club(models.Model):
   club_name = models.CharField(max_length=50)
   club_type = models.CharField(max_length=20)
   club_description = models.CharField(max_length=1000)
