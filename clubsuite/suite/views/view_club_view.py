from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from suite.models import Club
from suite.forms import EventCreateForm
from suite.models import Role
from suite.models import Event

from . import models


class ClubView(LoginRequiredMixin, TemplateView):
    form_class = EventCreateForm
    template_name = 'dashboard/club_view.html'

    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        form = self.form_class
        events = Event.objects.filter(cid=club_id)

        return render(request, self.template_name, {'club': club, 'form': form, 'events': events})

    def post(self, request, club_id):
      form = self.form_class(request.POST)
      club = get_object_or_404(Club, pk=club_id)
      if form.is_valid():
        event = form.save(club, commit=True)
        #role = Role(title='O', cid=club, uid=request.user).save()



      # create form with request
      events = Event.objects.filter(cid=club_id)
      return render(request, self.template_name, {'club': club, 'form' : form, 'events': events})
