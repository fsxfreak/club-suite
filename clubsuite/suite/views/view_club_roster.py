from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from suite.models import Club

class ClubRoster(LoginRequiredMixin, View):
  template_name = 'club_roster.html'
  def get(self, request, club_id, *args, **kwargs):
    club = get_object_or_404(Club, pk=club_id)
    roles = club.role_set.all()

    return render(request, self.template_name, {'club': club, 'roles' : roles })

