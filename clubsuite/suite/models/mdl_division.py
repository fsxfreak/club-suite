from django.db import models

from suite.models import Club

class Division(models.Model):
    cid = models.ForeignKey(
        'Club',
        on_delete = models.CASCADE,
        null=True
    )
    name = models.CharField(max_length=50, default="")
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name
