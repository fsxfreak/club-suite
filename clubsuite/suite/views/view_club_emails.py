from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.contrib import messages

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

  def get_members(self, club, group_str, actor):
    users = None
    if 'owner' in group_str.lower():
      users = club.get_owners().exclude(id=actor.id)
    elif 'officer' in group_str.lower():
      users = club.get_officers().exclude(id=actor.id)
    else: # 'members', ideally
      users = club.get_members().exclude(id=actor.id)

    members = []
    for user in users:
      group = club.get_group(user)
      members.append( {'user' : user, 'group' : group } )

    return members

  def get(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = self.get_members(club, 'members', request.user)


    return render(request, self.template_name, { 'club' : club, 'members': members})

  def post(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)


    if 'copied' in request.POST:
        messages.add_message(request, messages.SUCCESS, 'Emails Copied!')
        return render(request, self.template_name, {'club' : club})

    members = self.get_members(club, request.POST['member_type'], request.user)

    return render(request, self.template_name, {'club' : club, 'members': members})
