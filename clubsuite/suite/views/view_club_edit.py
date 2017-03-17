from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages

from suite.forms import ClubEditForm 
from suite.models import Club 

from guardian.shortcuts import get_perms
from django.core.exceptions import PermissionDenied

class ClubEdit(UserPassesTestMixin, LoginRequiredMixin, View):
  template_name = 'club_edit.html'
  form_class = ClubEditForm

  def test_func(self):
    club = get_object_or_404(Club, pk=self.kwargs['club_id'])
    if 'can_handle_promotion_requests' not in get_perms(self.request.user, club):
      raise PermissionDenied

    return True

  def get(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)
    form = self.form_class(instance=club)

    return render(request, self.template_name, { 'form' : form, 'club' : club })

  def post(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)
    old_club_name = club.club_name
    form = self.form_class(instance=club)

    if 'edit' in request.POST:
      form = self.form_class(request.POST, request.FILES, instance=club)
      if form.is_valid():
        club.update_group_names(old_club_name)
        club = form.save()

        return HttpResponseRedirect(reverse('suite:club_manage'))
      else:
        messages.add_message(request, messages.ERROR, 'Could not make changes to your club.')

    return render(request, self.template_name, { 'form' : form, 'club' : club })


