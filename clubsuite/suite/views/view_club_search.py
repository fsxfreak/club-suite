from django.http import HttpResponse
from django.views.generic import TemplateView

class ClubSearch(TemplateView):
    template_name = 'club_search.html'
