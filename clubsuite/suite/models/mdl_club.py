from django.db import models
from django.utils import timezone
from django.db.models import Q

class ClubManager(models.Manager):

   def qry_searchclubs(keyword):
      c=Club.objects.filter(
         Q(club_name__contains=keyword) |
         Q(club_description__contains=keyword)
      )
      r=c.objects.filter(club_type='PUB')
      return r

   def qry_searchoneclub(cid_in):
      c=Club.objects.get(id=cid_in)
      return c

class Club(models.Model):
   club_name = models.CharField(max_length=50,unique=True)

   
   C_CHOICES = (
       ('PUB','Public'),
       ('PRI','Private')
   )
    
   class Meta:
       permissions = (
           ("O", "Owner"),
           ("A", "Admin/Officer"),
           ("M", "Member"),
           ("P", "Passerby"),
           ('can_view_stats', 'Can view individual member stats'),
           ('can_create_event', 'Can create an event for this club'),
           ('can_add_receipt', 'Can add a receipt'),
           ('can_remove_receipt', 'Can remove a receipt'),
           ('can_access_attendance', 'Can access member attendance'),
           ('can_access_budget', 'Can access the budgets for this club'),
           ('can_create_budget', 'Can create a budget'),
           ('can_request_reimbusement', 'Can request for a reimbursement'),
           ('can_handle_reimbursement', 'Can handle reimbursement')
       )
   
   club_type = models.CharField(max_length=3,choices=C_CHOICES,default='PUB')
   image = models.ImageField(upload_to='media/', default="/media/default.jpg")
   first_seen = models.DateTimeField(editable=False, blank=True, null=True)
   last_seen = models.DateTimeField(blank=True, null=True)
   club_description = models.TextField()

   objects = ClubManager()

   def __str__(self):
       return self.club_name

   def summary(self):
       return self.club_description[:100]

   def save(self, *args, **kwargs):
       if not self.first_seen:
           self.first_seen = timezone.now()
       self.last_seen = timezone.now()
       return super(Club, self).save(*args, **kwargs)
