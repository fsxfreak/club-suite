from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from suite.forms import ClubCreateForm
from suite.models import Role

class ClubCreate(LoginRequiredMixin, View):
  form_class = ClubCreateForm
  template_name = 'club_create.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class
    return render(request, self.template_name, { 'form' : form })

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      club = form.save()
      role = Role(title='O', cid=club, uid=request.user).save()

      form.save()
      return HttpResponseRedirect(reverse('suite:dashboard'))

    # create form with request
    return render(request, self.template_name, { 'form' : form })

