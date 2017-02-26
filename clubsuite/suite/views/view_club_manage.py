from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse

from suite.models import Club, Role
from suite.forms import ClubJoinForm

class ClubManage(LoginRequiredMixin, View):
  template_name = 'dashboard/club_manage.html'

  def get_clubs(self, request):
    return request.user.club_set.all()

  def get(self, request, *args, **kwargs):
    clubs = self.get_clubs(request)
    return render(request, self.template_name, {'clubs' : clubs}) 

  def post(self, request, *args, **kwargs):
    if 'resign' in request.POST:
      roles = Role.objects.filter(cid=request.POST['club_id'], uid=request.user.id)
      roles.delete()

    clubs = self.get_clubs(request)
    return render(request, self.template_name, {'clubs' : clubs}) 

