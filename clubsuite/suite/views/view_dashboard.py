from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView
from suite.models import Club

class Dashboard(LoginRequiredMixin, TemplateView):
  def get(self, request):
    clubs = request.user.club_set.all()
    return render(request, 'dashboard/dashboard.html', { 'clubs': clubs, 'user': request.user})
