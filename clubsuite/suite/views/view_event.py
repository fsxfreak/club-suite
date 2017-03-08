from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import View

from suite.models import Event as EventModel
from suite.models import Club, EventSignIn, User

from guardian.shortcuts import get_perms

class Event(LoginRequiredMixin, View):
  template_name = 'event.html'

  def get(self, request, club_id, event_id, *args, **kwargs):
    club = get_object_or_404(Club, pk=club_id)
    event = EventModel.objects.get(pk=event_id)
    mems = club.members.all()
    eventSignIns = EventSignIn.objects.filter(eid=event_id, status=True)

    members = []
    for mem in mems:
      member = {'user': mem, 'group': club.get_group(mem)}
      if EventSignIn.objects.filter(eid=event_id, uid=mem, status=True).count() < 1:
        members.append(member)

    # getting the revnue
    totalCost = 0
    i = 1
    for eventSignIn in eventSignIns:
        totalCost = i * event.event_fee
        i+=1



    return render(request, self.template_name, {'club': club, 'members' : members,
     'event': event, 'eventSignIns': eventSignIns, 'totalCost':totalCost})

  def post(self, request, club_id, event_id, *args, **kwargs):
    club = get_object_or_404(Club, pk=club_id)

    if 'going' in request.POST and 'can_access_attendance' in get_perms(self.request.user, club):
      member_id = request.POST['going']
      event = EventModel.objects.get(pk=event_id)
      member = get_object_or_404(User, pk=member_id)

      eventsign = EventSignIn(cid=club, uid=member, eid=event, status=True)
      eventsign.save()

      return HttpResponseRedirect(reverse('suite:event',
        kwargs={ 'club_id': club_id, 'event_id': event_id}))

    return render(request, self.template_name, {'club': club, 'members' : members, 'event': event})
