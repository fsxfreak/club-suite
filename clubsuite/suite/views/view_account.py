from django.shortcuts import render, redirect
from suite.forms import RegistrationForm,EditProfileForm
from suite.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

class Account(View, LoginRequiredMixin):
  def get(self, request):
    if request.POST:
      if 'details' in request.POST:
        form = EditProfileForm(request.POST, instance=request.user)
        form.save()

      elif 'password' in request.POST:
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
          print('form valid')
          form.save()
          update_session_auth_hash(request, form.user)

    form = EditProfileForm(instance=request.user)
    form2 = PasswordChangeForm(user=request.user)
    args = {'form': form, 'form2': form2 }
    return render(request, 'account.html', args)

