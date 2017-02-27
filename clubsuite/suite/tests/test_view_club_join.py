from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubJoin
from suite.models import Club
from django.urls import reverse

class View_Club_Join_TestCase(TestCase):
    def setUp(self):
        self.client=Client()
        self.club=Club.objects.create(club_name="club",club_type="PUB", club_description="a club")


    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get_or_create(first_name='testuser')[0])
        response = self.client.get(reverse('suite:club_join',kwargs={'club_id':id(self.club)}))
        #self.assertRedirects(response,reverse('suite:club_join',self.club))

'''
    def test_get_not_logged_in(self):
        #response = self.client.get(reverse('suite:club_join'))
        self.assertRedirects(response,reverse('suite:club_join'))


'''
