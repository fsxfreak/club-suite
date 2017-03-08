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
        events = Event.objects.filter(cid=club_id).order_by('start_date')
        sign_ins = EventSignIn.objects.filter(cid=club_id, uid=request.user.id)
        signedInEvents = [sign_in.eid for sign_in in sign_ins ]
        signedInEvents = sorted(signedInEvents, key=lambda x: x.start_date, reverse=True)
        #if request[saved]:
        #    messages.add_message(request, messages.INFO, 'Made a club')

        return render(request, self.template_name, {'club': club, 'events': events, 'signedInEvents': signedInEvents})
