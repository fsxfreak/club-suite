from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.urls import reverse

from suite.models import Club, Division, Budget
from suite.forms import DivisionCreateForm, BudgetCreateForm

from guardian.shortcuts import get_perms
from django.core.exceptions import PermissionDenied

class Budget(UserPassesTestMixin, LoginRequiredMixin, View):
  template_name = 'dashboard/budget.html'
  division_form_class  = DivisionCreateForm
  budget_form_class = BudgetCreateForm

  def test_func(self):
    club = get_object_or_404(Club, pk=self.kwargs['club_id'])
    if 'can_access_budget' not in get_perms(self.request.user, club):
      raise PermissionDenied

    return True 

  def get(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)
    
    budget_form = self.budget_form_class()
    budget_form.fields['did'].queryset = Division.objects.filter(cid=club)

    division_form = self.division_form_class
    divisions = club.division_set.all()

    return render(request, self.template_name, { 'divisions' : divisions, 
                                                 'club': club,
                                                 'budget_form' : budget_form,
                                                 'division_form' : division_form})

  def post(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)

    budget_form = self.budget_form_class()
    division_form = self.division_form_class

    if 'division' in request.POST:
      division_form = self.division_form_class(request.POST)

      if division_form.is_valid():
        division = division_form.save()
        division.cid = club
        division.save()

    elif 'budget' in request.POST:
      budget_form = self.budget_form_class(request.POST)
      if budget_form.is_valid():
        budget = budget_form.save(commit=True)
        budget.save()

    divisions = club.division_set.all()
    return render(request, self.template_name, { 'divisions' : divisions, 
                                                 'club': club,
                                                 'budget_form' : budget_form,
                                                 'division_form' : division_form})


