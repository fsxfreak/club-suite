from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse

from suite.models import Club
from suite.forms import ClubJoinForm

class ClubJoin(LoginRequiredMixin, View):
  form_class = ClubJoinForm 
  template_name = 'club_join.html'

  def get(self, request, club_id, *args, **kwargs):
    form = self.form_class
    return render(request, self.template_name, { 'club_id' : club_id, 'form' : form })

  def post(self, request, club_id, *args, **kwargs):
    form = self.form_class(request.POST)

    if form.is_valid():
      reason = form.cleaned_data.get('reason')
      club = Club.objects.get(pk=club_id)

      # TODO DO A PENDING USERS

      redir = reverse('suite:club_view', args=[club_id])
      return HttpResponseRedirect(redir)

    return render(request, self.template_name, { 'form' : form })

