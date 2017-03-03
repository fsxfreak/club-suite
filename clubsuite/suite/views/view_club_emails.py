from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from suite.models import Club

class ClubEmails(LoginRequiredMixin, View):
  template_name = 'dashboard/club_emails.html'

  def get_members(self, club):
    members = []
    for member in club.members.all():
      group = Club.objects.get_group(club, member)
      members.append( {'user' : member, 'group' : group })

    return members

  def get_officers(self, club):
    members = []
    for member in Club.objects.get_officers(club):
      group = Club.objects.get_group(club, member)
      members.append( {'user' : member, 'group' : group })

    return members

  def get(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    members = self.get_members(club)
    return render(request, self.template_name, { 'club' : club, 'members': members})

  def post(self, request, club_id):
    members = None
    club = get_object_or_404(Club, pk=club_id)
    if request.POST['member_type'] == 'officer':
      members = self.get_officers(club)
    else:
      members = self.get_members(club)

    return render(request, self.template_name, {'club' : club, 'members': members})
