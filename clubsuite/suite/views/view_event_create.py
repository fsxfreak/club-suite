from django.http import HttpResponse
from django.views.generic import TemplateView

class EventCreate(TemplateView):
    template_name = 'event_create.html'
