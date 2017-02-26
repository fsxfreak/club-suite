from django.db import models

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

class Role(models.Model):
    # cid refers to the club object, not the club id
    cid = models.ForeignKey(
        'Club',
        on_delete=models.CASCADE
    )
    # uid refers to the user object, not the user id
    uid = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

    OWNER = 'O'
    OFFICER = 'A'
    MEMBER = 'M'
    PASSERBY = 'P'
    R_CHOICES = (
        (OWNER, 'Owner'),
        (OFFICER, 'Officer'),
        (MEMBER, 'Member'),
        (PASSERBY, 'Passerby')
    )
    title = models.CharField(
        max_length=1,
        choices=R_CHOICES,
        default=PASSERBY
    )

    objects = RoleManager()

    def __str__(self):
        s='User '+str(self.uid)+' is '+str(self.title)+\
          ' in Club '+str(self.cid)
        return s