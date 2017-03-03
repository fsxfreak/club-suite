from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from suite.models import Club

class ClubEmails(LoginRequiredMixin, View):
  template_name = 'dashboard/club_emails.html'

  def get_members(self, club, group_str):
    users = None
    if 'owner' in group_str:
      users = club.get_owners()
    elif 'officer' in group_str:
      users = club.get_officers()
    else: # 'members', ideally
      users = club.get_members()

    members = []
    for user in users:
      group = club.get_group(user)
      members.append( {'user' : user, 'group' : group } )

    return members

  def get(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = self.get_members(club, 'members')
    return render(request, self.template_name, { 'club' : club, 'members': members})

  def post(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)

    # 'member_type' see self.get_members function
    members = self.get_members(club, request.POST['member_type'])

    return render(request, self.template_name, {'club' : club, 'members': members})
