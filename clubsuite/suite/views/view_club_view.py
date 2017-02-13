from django.http import HttpResponse
from django.views.generic import TemplateView

class ClubView(TemplateView):
    template_name = 'club_view.html'
