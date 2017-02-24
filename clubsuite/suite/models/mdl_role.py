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

    OWNER = 'owner'
    OFFICER = 'officer'
    MEMBER = 'member'
    PASSERBY = 'passerby'
    REQUESTED = 'join'
    PROMOTE = 'promote'
#REQUESTED: the user has sent a request to this club and it's not been resolved
#yet. Accept -> Member, Deny -> Passerby
#PROMOTE: the member has sent a request to the officers of this club for a
#promotion and it's not been resolved yet. Accept -> Officer, Deny -> Member
    R_CHOICES = (
        (OWNER, 'Owner'),
        (OFFICER, 'Officer'),
        (MEMBER, 'Member'),
        (PASSERBY, 'Passerby'),
        (REQUESTED, 'Join Requested'),
        (PROMOTE, 'Promotion Requested')
    )
    title = models.CharField(
        max_length=10,
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
        club_members = club_users.exclude(title='passerby')
        return club_members

    # gives list of unresolved requests for joining this club
    def qry_requestlist(in_cid):
        club_record = Role.objects.filter(cid=in_cid)
        club_request = club_record.filter(title='join')
        return club_request

    # gives list of unresolved requests for promotion in this club
    def qry_promotelist(in_cid):
        club_record = Role.objects.filter(cid=in_cid)
        club_promote = club_record.filter(title='promote')
        return club_promote
