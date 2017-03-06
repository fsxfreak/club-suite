from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import View

from suite.models import Event as EventModel
from suite.models import Club, EventSignIn, User

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

    return render(request, self.template_name, {'club': club, 'members' : members, 
     'event': event, 'eventSignIns': eventSignIns})

  def post(self, request, club_id, event_id, *args, **kwargs):
    if 'going' in request.POST:
      member_id = request.POST['going']
      club = get_object_or_404(Club, pk=club_id)
      event = EventModel.objects.get(pk=event_id)
      member = get_object_or_404(User, pk=member_id)

      eventsign = EventSignIn(cid=club, uid=member, eid=event, status=True)
      eventsign.save()

      return HttpResponseRedirect(reverse('suite:event', 
        kwargs={ 'club_id': club_id, 'event_id': event_id}))

    return render(request, self.template_name, {'club': club, 'members' : members, 'event': event})
