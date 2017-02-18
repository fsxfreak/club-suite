from django.http import HttpResponse
from django.views.generic import TemplateView
from suite.models.mdl_user import *

class Signup(TemplateView):
    template_name = 'signup.html'
