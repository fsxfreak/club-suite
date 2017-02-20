from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from suite.forms import ClubSearchForm

class ClubSearch(LoginRequiredMixin, View):
  form_class = ClubSearchForm 
  template_name = 'club_search.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class
    # do query here
    return render(request, self.template_name, { 'form' : form })

