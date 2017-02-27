from django.db import models

class EventSignInManager(models.Manager):
    def get_attended_events(in_uid,in_cid):
        attended_eid=EventSignIn.objects.values_list('eid',
                        flat=True).filter(cid=in_cid,uid=in_uid)
        attended_events=Event.objects.filter(id__in=set(attended_eid)).order_by('-start_time')
        return attended_events

    def get_all_attended_events(in_uid):
        attended_eid=EventSignIn.objects.values_list('eid',
                        flat=True).filter(uid=in_uid)
        attended_events=Event.objects.filter(id__in=set(attended_eid)).order_by('-start_time')
        return attended_events

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

    objects = EventSignInManager()

    def __str__(self):
        s='User '+str(self.uid)+' Event '+str(self.eid)+\
          ' Club '+str(self.cid)
        return s
