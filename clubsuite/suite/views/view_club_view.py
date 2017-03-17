from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages

from suite.models import Club, Event, EventSignIn, JoinRequest
from . import models

class ClubView(LoginRequiredMixin, View):
    template_name = 'dashboard/club_view.html'

    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        reqs = Club.objects.get(pk=club_id).joinrequest_set.all()
        events = Event.objects.get_upcoming_events(club)
        signedInEvents = EventSignIn.objects.get_attended_events(request.user, club)

        return render(request, self.template_name, {'club': club, 'reqs': reqs, 'events': events, 'signedInEvents': signedInEvents})

    def post(self, request, club_id):
        if 'delete' in request.POST:
          event = Event.objects.get(id=request.POST['event_id'])
          event.delete()
          messages.add_message(request, messages.SUCCESS, 'Sucessfully deleted %s.' % event.event_name )

        club = get_object_or_404(Club, pk=club_id)
        reqs = Club.objects.get(pk=club_id).joinrequest_set.all()
        events = Event.objects.get_upcoming_events(club)
        signedInEvents = EventSignIn.objects.get_attended_events(request.user, club)

        return render(request, self.template_name, {'club': club, 'reqs': reqs, 'events': events, 'signedInEvents': signedInEvents})
