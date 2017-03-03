from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from suite.models import Club

class ClubEmails(LoginRequiredMixin, View):
  template_name = 'dashboard/club_emails.html'

  def get(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = []
    for member in club.members:
      members.append( {
        'full_name' : None
        , 'email' : None
        , 'group' : None
        }
      )

      return render(request, self.template_name, {'members': members})

  def post(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = []
    # TODO instead of members return officers
    for member in club.members:
      members.append( {
        'full_name' : None
        , 'email' : None
        , 'group' : None
        }
      )

    return render(request, self.template_name, {'members': members})
