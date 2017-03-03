from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from suite.models import Club, User

class ClubRoster(LoginRequiredMixin, View):
  template_name = 'club_roster.html'
  def get_members(self, club):
    members = []
    for member in club.members.all():
      group = club.get_group(member)
      members.append( {'user' : member, 'group' : group })

    return members

  def get(self, request, club_id, *args, **kwargs):
    club = get_object_or_404(Club, pk=club_id)
    members = self.get_members(club)

    return render(request, self.template_name, {'club': club, 'members' : members})

  def post(self, request, club_id, *args, **kwargs):
    club = get_object_or_404(Club, pk=club_id)

    if 'delete' in request.POST:
      user_id = request.POST['delete']
      club.remove_member(request.user, User.objects.get(id=user_id))
    elif 'promote' in request.POST:
      user_id = request.POST['promote']
      club.promote_to_officer(request.user, User.objects.get(id=user_id))

    members = self.get_members(club)
    return render(request, self.template_name, {'club': club, 'members' : members})

