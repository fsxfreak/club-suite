from django.http import HttpResponse
from django.views.generic import TemplateView

class About(TemplateView):
    template_name = 'about.html'
