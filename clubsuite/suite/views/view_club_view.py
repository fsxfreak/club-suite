from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages

from suite.models import Club, Event, EventSignIn
from . import models

class ClubView(LoginRequiredMixin, View):
    template_name = 'dashboard/club_view.html'

    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)

        events = Event.objects.get_upcoming_events(club)
        signedInEvents = EventSignIn.objects.get_attended_events(request.user, club)

        return render(request, self.template_name, {'club': club, 'events': events, 'signedInEvents': signedInEvents})
