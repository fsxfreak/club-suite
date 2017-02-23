from django.db import models
from django.utils import timezone
from django.db.models import Q

class Club(models.Model):
   club_name = models.CharField(max_length=50,unique=True)

   
   C_CHOICES = (
       ('PUB','Public'),
       ('PRI','Private')
   )
   """ 
   class Meta:
       permissions = (
           ("pub", "Public"),
           ("pri", "Private")
       )
   """
   club_type = models.CharField(max_length=3,choices=C_CHOICES,default='PUB')
   image = models.ImageField(upload_to='media/', default="/media/default.jpg")
   first_seen = models.DateTimeField(editable=False, blank=True, null=True)
   last_seen = models.DateTimeField(blank=True, null=True)
   club_description = models.TextField()

   def __str__(self):
       return self.club_name

   def summary(self):
       return self.club_description[:100]

   def save(self, *args, **kwargs):
       if not self.first_seen:
           self.first_seen = timezone.now()
       self.last_seen = timezone.now()
       return super(Club, self).save(*args, **kwargs)

   class ClubManager(models.Manager):

      def qry_searchclubs(keyword):
         r=Club.objects.filter(
            Q(club_name__contains=keyword) |
            Q(club_description__contains=keyword)
         )
         return r
