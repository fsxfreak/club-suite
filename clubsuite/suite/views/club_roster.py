from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView

class ClubRoster(LoginRequiredMixin, TemplateView):
  login_url = '/'
  template_name = 'club_roster.html'
