from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from suite.models import Club, Event, EventSignIn
from . import models

class ClubView(LoginRequiredMixin, View):
    template_name = 'dashboard/club_view.html'

    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        events = Event.objects.filter(cid=club_id)
        eventSignIn = EventSignIn.objects.filter(cid=club_id, uid=request.user.id)
        signedInEvents = [EventSignIn.eid for EventSignIn in eventSignIn]

        print(club)
        print(events)
        return render(request, self.template_name, {'club': club, 'events': events, 'signedInEvents': signedInEvents})
