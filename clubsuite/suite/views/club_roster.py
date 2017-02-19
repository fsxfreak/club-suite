from django.http import HttpResponse
from django.views.generic import TemplateView

class ClubRoster(TemplateView):
    template_name = 'club_roster.html'
