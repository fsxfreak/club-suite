from django.test import TestCase, RequestFactory
from django.test import Client
from suite.views import Account
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.messages.storage.fallback import FallbackStorage

class View_Account_TestCase(TestCase):
    def setUp(self):
        self.client=Client()
        self.request_factory=RequestFactory()

        #create user
        self.user=get_user_model().objects.create(first_name="User",last_name="McPerson",email="test@test.com")
        self.user.set_password("clubsuite")
        self.user.save()

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='User'))
        response = self.client.get(reverse('suite:edit_profile'))
        self.assertEqual(response.status_code,200)

    def test_post_edit_details(self):
        data={'details':'1', 'email':"test2@test.com",'first_name':"NewUser",'last_name':"Person",'instance':self.user}

        request=self.request_factory.post(reverse('suite:edit_profile'),data)
        request.user=self.user
        response=Account.as_view()(request)

        self.assertEqual(response.status_code,200)
        self.assertEqual(self.user.first_name,"NewUser")
        self.assertEqual(self.user.last_name,"Person")
        self.assertEqual(self.user.email,"test2@test.com")


    def test_post_edit_password(self):
        self.client.force_login(get_user_model().objects.get(first_name='User'))

        data={'password':'1', 'old_password':"clubsuite",'new_password1':"clubsuite1",'new_password2':"clubsuite1"}

        response=self.client.post(reverse('suite:edit_profile'),data)

        self.assertEqual(response.status_code,200)
        #Need get() to get updated user
        newUser=get_user_model().objects.get(first_name='User')
        self.assertEqual(newUser,self.user)
        self.assertTrue(check_password("clubsuite1",newUser.password))

