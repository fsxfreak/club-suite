from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
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

  def generate_books(self, divs):
    books = []
    for div in divs:
      budgets = div.budget_set.all()
      total_budget = 0
      for budget in budgets:
        total_budget = total_budget + budget.planned

      events = div.event_set.all()
      total_expense = 0
      for event in events:
        total_expense = total_expense + event.event_cost

      books.append({ 'division' : div, 'budgets' : budgets, 'events' : events,
        'total_budget' : total_budget, 'total_expense' : total_expense })

    return books

  def get(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)

    budget_form = self.budget_form_class()
    budget_form.fields['did'].queryset = Division.objects.filter(cid=club)

    division_form = self.division_form_class

    books = self.generate_books(club.division_set.all())

    total_budget = 0
    total_expense = 0
    for book in books:
      total_budget = total_budget + book['total_budget']
      total_expense = total_expense + book['total_expense']

    return render(request, self.template_name, { 'books': books,
                                                 'club': club,
                                                 'budget_form' : budget_form,
                                                 'division_form' : division_form,
                                                 'total_budget' : total_budget,
                                                 'total_expense' : total_expense})

  def post(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)

    budget_form = self.budget_form_class()
    budget_form.fields['did'].queryset = Division.objects.filter(cid=club)

    division_form = self.division_form_class

    if 'division' in request.POST:
      division_form = self.division_form_class(request.POST)

      if division_form.is_valid():
        division = division_form.save()
        division.cid = club
        division.save()
        messages.add_message(request, messages.SUCCESS, 'You Have Created a New Division!')
        return HttpResponseRedirect(reverse('suite:budget', args=[club_id]))
      else:
        messages.add_message(request, messages.WARNING, 'Cannot Make Division with Same Name')
        return HttpResponseRedirect(reverse('suite:budget', args=[club_id]))

    elif 'budget' in request.POST:
      budget_form = self.budget_form_class(request.POST)
      if budget_form.is_valid():
        budget = budget_form.save(commit=True)
        budget.save()
      else:
        messages.add_message(request, messages.WARNING, 'Could not create budget.')
      budget_form.fields['did'].queryset = Division.objects.filter(cid=club)

    books = self.generate_books(club.division_set.all())
    total_budget = 0
    total_expense = 0
    for book in books:
      total_budget = total_budget + book['total_budget']
      total_expense = total_expense + book['total_expense']

    return render(request, self.template_name, { 'books' : books,
                                                 'club': club,
                                                 'budget_form' : budget_form,
                                                 'division_form' : division_form,
                                                 'total_budget' : total_budget,
                                                 'total_expense' : total_expense})
