from django.http import HttpResponse
from django.views.generic import TemplateView

class ClubCreate(TemplateView):
    template_name = 'club_create.html'
