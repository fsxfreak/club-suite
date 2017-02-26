from django.db import models
from django.utils import timezone

from suite.models import User

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
    club_name = models.CharField(max_length=50)
    
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

    objects = ClubManager()
    members = models.ManyToManyField(User, through='Role')

    def __str__(self):
         return self.club_name
 
    def summary(self):
        if len(self.club_description) < 150:
            return self.club_description;
        else:
            unformatted_summary = self.club_description[:150];
            last_index = len(unformatted_summary) - 1;
            while( last_index >= 0 and unformatted_summary[last_index] != ' ' ):
                last_index = last_index - 1;
            unformatted_summary += "...";
            return unformatted_summary;

    def save(self, *args, **kwargs):
        if not self.first_seen:
            self.first_seen = timezone.now()
        self.last_seen = timezone.now()
        return super(Club, self).save(*args, **kwargs)
