from django.contrib import auth
from django import forms
from .models import User

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

        print(user.get_custom())
        if commit:
            user.save()
        return user 
