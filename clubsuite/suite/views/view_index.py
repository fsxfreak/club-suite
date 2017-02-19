from django.http import HttpResponse
from django.views.generic import TemplateView

from django.contrib.auth import authenticate

def view_index(request):
  user = authenticate(email='admin2@admin2.com', password='administrator2')
  if user is not None:
    print('authenticate')
    # A backend authenticated the credentials
  else:
    print('no authenticate')
    # No backend authenticated the credentials

class Index(TemplateView):
    template_name = 'registration/login.html'
