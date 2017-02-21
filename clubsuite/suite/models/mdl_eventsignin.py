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

    def __str__(self):
        s='User '+str(self.uid)+' Event '+str(self.eid)+\
          ' Club '+str(self.cid)
        return s
