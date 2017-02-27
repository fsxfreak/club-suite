from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from suite.models import Club

from suite.forms import EventCreateForm

class ClubView(LoginRequiredMixin, TemplateView):
    form_class = EventCreateForm
    template_name = 'dashboard/club_view.html'

    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        form = self.form_class
        return render(request, self.template_name, {'club': club, 'form': form})

    def post(self, request, *args, **kwargs):
      form = self.form_class(request.POST)
      if form.is_valid():
        event = form.save()

        form.save()
        return HttpResponseRedirect(reverse('suite:dashboard'))

      # create form with request
      return render(request, self.template_name, {'club': club}, { 'form' : form })
