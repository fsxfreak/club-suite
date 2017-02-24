from django.shortcuts import render, redirect
from suite.forms import RegistrationForm,EditProfileForm
from suite.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class Account:
    #template_name = 'account.html'

    def edit_profile(request):
        if request.POST:
            print(request.POST)
            if 'details' in request.POST:
                form = EditProfileForm(request.POST, instance=request.user)
                form.save()
            elif 'password' in request.POST:
                form = PasswordChangeForm(request.POST)
                form.save()
            return redirect('/account')
        else:
            form = EditProfileForm(instance=request.user)
            form2 = PasswordChangeForm(user=request.user)
            args = {'form': form, 'form2': form2 }
            return render(request, 'account.html',args)

'''
            if form.is_valid():
                form.save()
                return redirect('/account')
            else:
                print(form)
                return redirect('/dashboard')
'''
