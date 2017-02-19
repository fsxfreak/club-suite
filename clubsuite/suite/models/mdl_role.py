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

