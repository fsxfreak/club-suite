from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View

from suite.models import Club

from guardian.shortcuts import get_perms
from django.core.exceptions import PermissionDenied

class ClubEmails(UserPassesTestMixin, LoginRequiredMixin, View):
  template_name = 'dashboard/club_emails.html'

  def test_func(self):
    club = get_object_or_404(Club, pk=self.kwargs['club_id'])
    if 'can_view_account_info' not in get_perms(self.request.user, club):
      raise PermissionDenied

    return True 

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
