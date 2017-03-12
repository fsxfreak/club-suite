from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages

from suite.forms import EventEditForm 
import suite.models

from guardian.shortcuts import get_perms
from django.core.exceptions import PermissionDenied

class EventEdit(UserPassesTestMixin, LoginRequiredMixin, View):
  template_name = 'event_edit.html'
  form_class = EventEditForm 

  def test_func(self):
    club = suite.models.Club.objects.get(pk=self.kwargs['club_id'])
    if 'can_create_event' not in get_perms(self.request.user, club):
      raise PermissionDenied

    return True

  def get(self, request, club_id, event_id, *args, **kwargs):
    club = suite.models.Club.objects.get(pk=club_id)
    event = suite.models.Event.objects.get(pk=event_id)
    form = self.form_class(instance=event)

    return render(request, self.template_name, { 'form' : form, 
                                                 'club' : club,
                                                 'event' : event})

  def post(self, request, club_id, event_id, *args, **kwargs):
    club = suite.models.Club.objects.get(pk=club_id)
    event = suite.models.Event.objects.get(pk=event_id)
    form = self.form_class(instance=event)

    if 'edit' in request.POST:
      form = self.form_class(request.POST, request.FILES, instance=event)
      if form.is_valid():
        event = form.save()
        print('valid')

        messages.add_message(request, messages.SUCCESS, 'Successfully edited event.')
        return HttpResponseRedirect(reverse('suite:club_view', 
          kwargs={'club_id': club.id }))
      else:
        messages.add_message(request, messages.ERROR, 'Could not make changes to your event.')

    return render(request, self.template_name, { 'form' : form, 
                                                 'club' : club,
                                                 'event' : event})



