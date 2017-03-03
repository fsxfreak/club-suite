from django.contrib import auth
from django import forms

from django.contrib.auth.forms import UserChangeForm
from .models import *

class RegistrationForm(auth.forms.UserCreationForm):
  class Meta:
    model = User
    fields = ['first_name','last_name','email', 'password1', 'password2']

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

  def clean_password2(self):
    # Check that the two password entries match
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")

    if password1 and password2 and password1 != password2:
      msg = "Passwords don't match"
      raise forms.ValidationError("Password mismatch")

    return password2

  def save(self, commit=False):
    user = super(RegistrationForm, self).save(commit=False)
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.email = self.cleaned_data['email']
    user.set_password(self.cleaned_data['password1'])
    user.is_active = True

    # more account stuff needed here
    user.account = Account(student_title='U',
                           preferred_name=self.cleaned_data['first_name'])

    if commit:
      user.save()
    return user

# good docs
# https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
class ClubCreateForm(forms.ModelForm):
  class Meta:
    model = Club
    fields = ['club_name', 'club_type', 'club_description', 'image' ]

class EventCreateForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = ['event_name', 'start_time', 'end_time', 'event_location',
    'event_description', 'event_cost', 'accessibility', 'required']

  def save(self, club, commit=False):

      event_name = self.cleaned_data['event_name']
      start_time = self.cleaned_data['start_time']
      end_time = self.cleaned_data['end_time']
      event_location = self.cleaned_data['event_location']
      event_description = self.cleaned_data['event_description']
      event_cost = self.cleaned_data['event_cost']
      accessibility = self.cleaned_data['accessibility']
      required = self.cleaned_data['required']

      event_cid = Event(cid=club, event_name=event_name, start_time=start_time,
      end_time=end_time, event_location=event_location, event_description=event_description,
      event_cost=event_cost, accessibility=accessibility, required=required)
      if commit:
          event_cid.save()

      return event_cid

  #def clean():
  # validation

class ClubSearchForm(forms.Form):
  club_name = forms.CharField(max_length=50, required=False)
  keyword = forms.CharField(max_length=50,
                            required=False,
                            label='Club name or description')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name' ]

class ClubJoinForm(forms.Form):
  reason = forms.CharField(max_length=50,
                           required=True)
