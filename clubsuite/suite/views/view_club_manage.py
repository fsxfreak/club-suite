from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse

from suite.models import Club
from suite.forms import ClubJoinForm

class ClubManage(LoginRequiredMixin, View):
  template_name = 'dashboard/club_manage.html'

  def get(self, request, *args, **kwargs):
    clubs = request.user.get_clubs()
    return render(request, self.template_name, {'clubs' : clubs}) 

  def post(self, request, *args, **kwargs):
    if 'resign' in request.POST:
      club = Club.objects.get(id=request.POST['club_id'])
      club.remove_member(request.user, request.user)

    clubs = request.user.get_clubs()
    return render(request, self.template_name, {'clubs' : clubs}) 

