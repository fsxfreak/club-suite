from django.db import models

class Budget(models.Model):
    cid = models.ForeignKey(
        'Club',
        on_delete = models.CASCADE
    )

    did = models.ForeignKey('Division')

    planned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    used = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        s=str(self.cid)+' '+str(self.did)+' '+str(self.planned)
        return "Club and Division and Plan: "+s

