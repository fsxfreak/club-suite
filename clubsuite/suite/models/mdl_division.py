from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=50, default="name for this division",\
           primary_key=True)
