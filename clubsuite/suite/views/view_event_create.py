from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404

from suite.models import Club

class EventCreate(TemplateView):
    template_name = 'event_create.html'

    def get(self, request, club_id):
      club = get_object_or_404(Club, pk=club_id)
      return render(request, self.template_name, { 'club' : club })

    def post(self, request, club_id):
      form = self.form_class(request.POST)
      club = get_object_or_404(Club, pk=club_id)
      if form.is_valid():
        event = form.save(club, commit=True)

