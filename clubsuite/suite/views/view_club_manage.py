from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse

from suite.models import Club, Role
from suite.forms import ClubJoinForm

class ClubManage(LoginRequiredMixin, View):
  template_name = 'dashboard/club_manage.html'

  def get(self, request, *args, **kwargs):
    user_roles = request.user.role_set.all()
    print(user_roles)

    clubs = None

    return render(request, self.template_name, {'clubs' : clubs}) 

  def post(self, request, *args, **kwargs):
    # should allow resignation from club.
    pass

