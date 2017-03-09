from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from suite.models import Club, Division, Budget
from suite.forms import EventCreateForm
from django.contrib import messages

from guardian.shortcuts import get_perms
from django.core.exceptions import PermissionDenied

class EventCreate(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
  form_class = EventCreateForm
  template_name = 'event_create.html'

  # testing for proper permissions
  def test_func(self):
    club = get_object_or_404(Club, pk=self.kwargs['club_id'])
    if 'can_create_event' not in get_perms(self.request.user, club):
      raise PermissionDenied

    return True

  def get(self, request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    form = self.form_class()
    form.fields['did'].queryset = Division.objects.filter(cid=club)

    return render(request, self.template_name, { 'club' : club, 'form' : form})

  def post(self, request, club_id):
    form = self.form_class(request.POST, request.FILES)
    club = get_object_or_404(Club, pk=club_id)
    if form.is_valid():
      event = form.save(club, commit=True)
      messages.add_message(request, messages.SUCCESS, 'You Have Created an Event!')
      #saved = True
    else:
      return render(request, self.template_name, { 'club' : club, 'form' : form})

    return HttpResponseRedirect(reverse('suite:club_view', args=[club_id]))
