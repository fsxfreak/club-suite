from django.test import TestCase
from suite import RegistrationForm
# Create your tests here.
#

class RegistrationFormTestCase(TestCase):
    def setUp(self):
        RegistrationForm.objects.create(email="test@test.com",password1="pass",password2="pass")

    def test_registration_form(self):
        reg_email=RegistrationForm.objects.get(email)
        self.assertEqual(reg_email.email,"test@test.com")
