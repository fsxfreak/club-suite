from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView
from suite.models import Club


class ClubView(LoginRequiredMixin, TemplateView):
    def get(self, request, club_id):
        club = get_object_or_404(Club, pk=club_id)
        return render(request, 'dashboard/club_view.html', {'club': club})
