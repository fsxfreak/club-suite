from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from suite.forms import ClubCreateForm

class ClubCreate(LoginRequiredMixin, View):
  form_class = ClubCreateForm
  template_name = 'club_create.html'


  def get(self, request, *args, **kwargs):
    form = self.form_class
    return render(request, self.template_name, { 'form' : form })

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST, request.FILES)
    if form.is_valid():
      club = form.save()
      club._create_permissions()
      club._set_owner(request.user)
      messages.add_message(request, messages.SUCCESS, 'You Have Created a Club!')

      return HttpResponseRedirect(reverse('suite:dashboard'))

    # create form with request
    return render(request, self.template_name, { 'form' : form })
