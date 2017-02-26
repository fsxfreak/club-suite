from django.db import models

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
        (PASSERBY, 'Passerby'),
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
