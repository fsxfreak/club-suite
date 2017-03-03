from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from suite.models import Club

class ClubEmails(LoginRequiredMixin, View):
  template_name = 'dashboard/club_emails.html'

  def get_members(self, club):
    members = []
    for member in club.members.all():
      members.append( {'user' : member, 'group' : None })

    return members

  def get(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = self.get_members(club)
    print(members)
  
    return render(request, self.template_name, {'members': members})

  def post(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = []
    # TODO instead of members return officers
    members = self.get_members(club)

    return render(request, self.template_name, {'members': members})
