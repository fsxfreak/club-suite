from django.shortcuts import render, redirect
from suite.forms import RegistrationForm,EditProfileForm
from suite.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

class Account(View, LoginRequiredMixin):
  def get(self, request):
    form = EditProfileForm(instance=request.user)
    form2 = PasswordChangeForm(user=request.user)
    args = {'form': form, 'form2': form2 }
    return render(request, 'account.html', args)

  def post(self, request):

    if 'details' in request.POST:
      form = EditProfileForm(request.POST, instance=request.user)
      if form.is_valid():
        form.save()
      else:
        messages.add_message(request, messages.ERROR, 'Could not edit account details.')

      form2 = PasswordChangeForm(user=request.user)
      args = {'form': form, 'form2': form2 }
      return render(request, 'account.html', args)

    elif 'password' in request.POST:
      form2 = PasswordChangeForm(user=request.user, data=request.POST)
      if form2.is_valid():
        form2.save()
        update_session_auth_hash(request, form2.user)
        messages.add_message(request, messages.SUCCESS, 'Sucessfully changed password.')
      else:
        messages.add_message(request, messages.ERROR, 'Password change unsuccessful.')

      form = EditProfileForm(instance=request.user)
      args = {'form': form, 'form2': form2 }
      return render(request, 'account.html', args)

