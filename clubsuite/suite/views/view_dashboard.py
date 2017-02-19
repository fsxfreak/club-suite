from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView

class Dashboard(LoginRequiredMixin, TemplateView):
  login_url = 'suite:login'
  template_name = 'dashboard.html'
