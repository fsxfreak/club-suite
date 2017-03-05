from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubCreate
from django.urls import reverse
from suite.models import Club

class View_Club_Search_TestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.club=Club.objects.create(club_name="Cool club",club_type="PUB",club_description="a club")

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get_or_create(first_name='testuser')[0])
        response = self.client.get(reverse('suite:club_search'))
        self.assertEqual(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:club_search'))
        self.assertRedirects(response, "/?next="+reverse('suite:club_search'), 302,200)

    def test_post(self):
        self.client.force_login(get_user_model().objects.get_or_create(first_name='testuser')[0])
        data = {'keyword':"club"}
        response = self.client.post(reverse('suite:club_search'),data, follow=True)
        self.assertContains(response,"Cool club")

    def test_post_no_club(self):
        self.client.force_login(get_user_model().objects.get_or_create(first_name='testuser')[0])
        # no club name
        data = {'keyword':"test"}
        response = self.client.post(reverse('suite:club_search'),data, follow=True)
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response,"Cool club")
