from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages

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
      if not club.remove_member(request.user, User.objects.get(id=user_id)):
          messages.add_message(request, messages.ERROR, 'Cannot delete only owner')
    elif 'promote' in request.POST:
      user_id = request.POST['promote']
      act_on_user = User.objects.get(id=user_id)
      if not club.is_officer(act_on_user):
        club.promote_to_officer(request.user, act_on_user)
      elif club.is_officer(act_on_user):
        club.promote_officer_to_owner(request.user, act_on_user)
    elif 'demote' in request.POST:
      user_id = request.POST['demote']
      act_on_user = User.objects.get(id=user_id)
      if club.is_owner(act_on_user):
        if not club.demote_owner_to_officer(request.user, act_on_user):
            messages.add_message(request, messages.ERROR, 'You Cannot Demote Yourself!')
      elif club.is_officer(act_on_user):
        club.demote_from_officer(request.user, act_on_user)

    members = self.get_members(club)
    return render(request, self.template_name, {'club': club, 'members' : members})
