from django.db import models

class Role(models.Model):
    cid = models.ForeignKey(
        'Club',
        on_delete=models.CASCADE
    )
    
    uid = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

    OWNER = 'O'
    OFFICER = 'A'
    MEMBER = 'M'
    PASSERBY = 'P'
    REQUESTED = 'R'
#Requested: the user has sent a request to this club and it's not been resolved
#yet. Accept -> Member, Deny -> Passerby
    R_CHOICES = (
        (OWNER, 'Owner'),
        (OFFICER, 'Officer'),
        (MEMBER, 'Member'),
        (PASSERBY, 'Passerby'),
        (REQUESTED, 'Requested')
    )
    title = models.CharField(
        max_length=1,
        choices=R_CHOICES,
        default=PASSERBY
    )

    def __str__(self):
        s='User '+str(self.uid)+' is '+str(self.title)+\
          ' in Club '+str(self.cid)
        return s
  
class RoleManager(models.Manager):
    def qry_clubmembers(in_cid):
        club_users = Role.objects.filter(cid=in_cid)
        club_members = club_users.exclude(title='P')
        return club_members

    # gives list of unresolved requested of this club
    def qry_requestlist(in_cid):
        club_record = Role.objects.filter(cid=in_cid)
        club_request = club_record.filter(title='R')
        return club_request
