from django.db import models

class EventSignIn(models.Model):
    status = models.BooleanField(default=False)
    cid = models.ForeignKey(
        'Club',
        on_delete = models.CASCADE,
    )
    eid = models.ForeignKey(
        'Event',
        on_delete = models.CASCADE,
    )
    uid = models.ForeignKey(
        'User',
        on_delete = models.CASCADE,
    )
