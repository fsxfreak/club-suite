from django.test import TestCase
from suite.forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import Client
# Create your tests here.
#

class RegistrationFormTestCase(TestCase):
    def setUp(self):
        pass

    def test_valid_data(self):
        form=RegistrationForm(data={'email':"test@test.com",
                                'password1':"clubsuite",
                                'password2':"clubsuite",
                                'first_name':"First",
                                'last_name':"Last"})
        user=form.save()

        self.assertTrue(form.is_valid())
        self.assertTrue(user.email=="test@test.com")
        self.assertTrue(check_password("clubsuite",user.password))
        self.assertTrue(user.first_name, "First")
        self.assertTrue(user.last_name, "Last")
