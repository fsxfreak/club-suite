from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from suite.forms import ClubSearchForm
from suite.models import qry_searchclubs

class ClubSearch(LoginRequiredMixin, View):
  form_class = ClubSearchForm 
  template_name = 'club_search.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class
    return render(request, self.template_name, { 'form' : form })

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    clubs = None

    if form.is_valid():
      keyword = form.cleaned_data.get('keyword')
      clubs = qry_searchclubs(keyword)

      print(clubs)

    return render(request, self.template_name, { 'form' : form, 'clubs' : clubs })

