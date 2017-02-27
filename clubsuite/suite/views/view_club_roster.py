from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from suite.models import Club

class ClubRoster(LoginRequiredMixin, View):
  template_name = 'club_roster.html'
  def get(self, request, club_id, *args, **kwargs):
    club = get_object_or_404(Club, pk=club_id)
    mems = club.members.all()

    members = []
    for mem in mems:
      member = {'user': mem, 'group': None } # TODO group
      print(member)
      members.append(member)

    print(members)

    return render(request, self.template_name, {'club': club, 'members' : members})

