'''
from django.test import TestCase
from suite.models import UserManager
# Create your tests here.
#

class UserManagerTestCase(TestCase):
    def setUp(self):
        UserManager.objects.create(email="test@test.com",password="pass")

    def test_UserManager(self):
        reg_email=UserManager.objects.get(email)
        self.assertEqual(reg_email.email,"test@test.com")
        '''
