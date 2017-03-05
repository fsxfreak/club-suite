from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import View

from suite.models import Event as EventModel
from suite.models import Club
from suite.models import EventSignIn
from suite.models import User
from . import models

class Event(LoginRequiredMixin, View):
    template_name = 'event.html'


    def test_func(self):
        club = get_object_or_404(Club, pk=self.kwargs['club_id'])
        if 'can_handle_join_requests' not in get_perms(self.request.user, club):
            raise PermissionDenied

        return True

    def get(self, request, club_id, event_id, *args, **kwargs):
       #
       club = get_object_or_404(Club, pk=club_id)
       event = EventModel.objects.get(pk=event_id)
       mems = club.members.all()
       eventSignIns = EventSignIn.objects.filter(eid=event_id)

       members = []
       for mem in mems:
         member = {'user': mem, 'group': None } # TODO group
         print(member)
         members.append(member)

       print(members)

       return render(request, self.template_name, {'club': club, 'members' : members, 'event': event, 'eventSignIns': eventSignIns})

    def post(self, request, club_id, event_id, *args, **kwargs):
        if 'going' in request.POST:
            member_id = request.POST['going']
            club = get_object_or_404(Club, pk=club_id)
            event = EventModel.objects.get(pk=event_id)
            member = get_object_or_404(User, pk=club_id)

            #i want to then create an eventsign in object with the user id, event id, and then club id
            eventsign = EventSignIn(cid=club, uid=member, eid=event, status=True)
            return HttpResponseRedirect(reverse('suite:event', args=[club_id, event_id]))

        return render(request, self.template_name, {'club': club, 'members' : members, 'event': event})
