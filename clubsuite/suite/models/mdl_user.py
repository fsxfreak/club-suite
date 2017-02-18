from django.db import models

class User(models.Model):
   password = models.CharField(max_length=20)
   first_name = models.CharField(max_length=20)
   last_name = models.CharField(max_length=20)
   email = models.CharField(max_length=30)

class Account(models.Model):
   user = models.OneToOneField(
      User, 
      on_delete = models.CASCADE,
      primary_key = True,
   )
   preferred_name = models.CharField(max_length=20, blank=True)
   graduation_year = models.IntegerField(blank=True)
   major = models.CharField(max_length=20, blank=True)
   college = models.CharField(max_length=50, blank=True)
   GPA = models.DecimalField(max_digits=4, decimal_places=3, blank=True)
