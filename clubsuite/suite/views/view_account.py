from django.http import HttpResponse
from django.views.generic import TemplateView

class Account(TemplateView):
    template_name = 'account.html'
