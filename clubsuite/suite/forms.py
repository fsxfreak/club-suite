from django.contrib import auth
from django import forms

from .models import User, Club

class RegistrationForm(auth.forms.UserCreationForm):
  class Meta:
    model = User
    fields = ['email', 'password1', 'password2']

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
      user.email = self.cleaned_data['email']
      user.set_password(self.cleaned_data['password1'])
      user.is_active = True
      if commit:
        user.save()
      return user 

# good docs
# https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
class ClubCreateForm(forms.ModelForm):
  class Meta:
    model = Club
    fields = ['club_name', 'club_type', 'club_description' ]

  #def clean():
  # validation

class ClubSearchForm(forms.Form):
  club_name = forms.CharField(max_length=50)
