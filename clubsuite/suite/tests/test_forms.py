from django.test import TestCase
from suite.forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
# Create your tests here.
#

class RegistrationFormTestCase(TestCase):
    #def setUp(self):
        #User=get_user_model().objects.create(email="test@test.com",password1="pasdd",password2="pasdd")
        #RegistrationForm.objects.create(email="test@test.com",password1="pass",password2="pass")


    def test_valid_data(self):
        form=RegistrationForm(data={'email':"test@test.com",
                                'password1':"clubsuite",
                                'password2':"clubsuite"})
                                
        
        #print(form.errors)#debug
        #self.assertTrue(form.fields['email']=="test@test.com")
        self.assertTrue(form.is_valid())
        user=form.save()
        
        #print(user.email) #debug
        self.assertTrue(user.email=="test@test.com")
        self.assertTrue(check_password("clubsuite",user.password))
        
