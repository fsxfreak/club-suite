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

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            # password reset email look
            'email_template_name': 'registration/verification.html',
            # password reset email subject
            'subject_template_name': 'registration/verification_subject.txt',
            'request': self.request,
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect('suite:register_done')
