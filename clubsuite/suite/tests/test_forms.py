from django.test import TestCase
from suite.forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import Client
# Create your tests here.
#

class RegistrationFormTestCase(TestCase):
    def setUp(self):
        # does this run?
        User=get_user_model().objects.create(email="test@test.com",password1="pasdd",password2="pasdd")
        
    def test_valid_data(self):
        form=RegistrationForm(data={'email':"test@test.com",
                                'password1':"clubsuite",
                                'password2':"clubsuite"})
        user=form.save()
                                
        self.assertTrue(form.is_valid())
        self.assertTrue(user.email=="test@test.com")
        self.assertTrue(check_password("clubsuite",user.password))