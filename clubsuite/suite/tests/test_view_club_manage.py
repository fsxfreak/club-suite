from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubManage
from django.urls import reverse
from suite.models import Club

class View_Club_Manage_TestCase(TestCase):
    def setUp(self):
        self.client = Client()

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #create club owner2, since owner can only resign if there is more than 1 owner
        self.owner2=get_user_model().objects.create(first_name="Owner2",last_name="McPerson",email="test2@test.com")
        self.owner2.set_password("clubsuite")
        self.owner2.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)
        self.club._set_owner(self.owner2)


    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name="Owner"))
        response = self.client.get(reverse('suite:club_manage'))
        self.assertEqual(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:club_manage'))
        self.assertRedirects(response, "/?next="+reverse('suite:club_manage'),302,200)

    def test_post_login_resign(self):
        self.assertTrue(self.club.is_owner(self.owner))
        self.client.force_login(get_user_model().objects.get(first_name="Owner"))

        data = {'resign':"",
                'club_id':self.club.pk}


        response = self.client.post(reverse('suite:club_manage'),data,follow=True)
        self.assertFalse(self.club.is_owner(self.owner))
        self.assertFalse(self.club.is_officer(self.owner))
        self.assertFalse(self.club.is_member(self.owner))

        self.assertEqual(response.status_code,200)

    def test_post_login_no_resign(self):
        self.assertTrue(self.club.is_owner(self.owner))
        self.client.force_login(get_user_model().objects.get(first_name="Owner"))

        data = {'club_id':self.club.pk}

        response = self.client.post(reverse('suite:club_manage'),data,follow=True)
        self.assertTrue(self.club.is_owner(self.owner))
        self.assertTrue(self.club.is_officer(self.owner))
        self.assertTrue(self.club.is_member(self.owner))
        self.assertEqual(response.status_code,200)
