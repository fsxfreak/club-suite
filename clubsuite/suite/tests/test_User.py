from django.test import TestCase
from suite.models import UserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(first_name="First",last_name="Last",email="test@test.com")
        self.user.set_password("testclub123")
        self.user.save()

    def test_user(self):
        #reg_email=UserManager.objects.get(email)
        self.assertEqual(self.user.email,"test@test.com")
        self.assertEqual(self.user.get_short_name(),"First")
        self.assertEqual(self.user.get_full_name(),"First Last")
        self.assertEqual(self.user.last_name,"Last")
        self.assertTrue(check_password("testclub123",self.user.password))
