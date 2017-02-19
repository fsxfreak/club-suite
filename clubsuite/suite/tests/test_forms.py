from django.test import TestCase
from suite.forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.test import Client
# Create your tests here.
#

class RegistrationFormTestCase(TestCase):
    def setUp(self):
        User=get_user_model().objects.create(email="test@test.com",password1="pasdd",password2="pasdd")
        #RegistrationForm.objects.create(email="test@test.com",password1="pass",password2="pass")


    def test_valid_data(self):
        form=RegistrationForm(data={'email':"test@test.com",
                                'password1':"pass",
                                'password2':"pass"})
        self.assertTrue(form.is_valid())
        '''
        registration=form.save()

        self.assertTrue(form.password1=="pass")
        self.assertTrue(form.password2=="pass")
        '''
