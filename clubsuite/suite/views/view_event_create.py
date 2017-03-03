from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from suite.models import Club
from suite.forms import EventCreateForm

class EventCreate(TemplateView):
    form_class = EventCreateForm
    template_name = 'event_create.html'

    def get(self, request, club_id):
      club = get_object_or_404(Club, pk=club_id)
      form = self.form_class
      return render(request, self.template_name, { 'club' : club, 'form' : form})

    def post(self, request, club_id):
      form = self.form_class(request.POST)
      club = get_object_or_404(Club, pk=club_id)
      if form.is_valid():
        event = form.save(club, commit=True)

      return HttpResponseRedirect(reverse('suite:club_view', args=[club_id]))

