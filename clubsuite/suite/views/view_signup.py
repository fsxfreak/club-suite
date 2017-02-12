from django.http import HttpResponse
from django.views.generic import TemplateView

class Signup(TemplateView):
    template_name = 'signup.html'
