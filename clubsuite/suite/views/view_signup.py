from django.http import HttpResponse
from django.views.generic import TemplateView
from suite.models.mdl_user import *

from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.views.generic import CreateView

from suite.forms import RegistrationForm
from suite.models import User

class RegistrationView(CreateView):
  template_name = 'registration/register.html'
  form_class = RegistrationForm
  model = User

  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.save()

    return redirect('suite:register_done')
