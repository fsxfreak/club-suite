from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubView
from django.urls import reverse
from suite.models import Club
from suite.models import Event

class View_Club_View_TestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.club=Club.objects.create(club_name="Cool club",club_type="PUB",club_description="a club")

        self.event = Event.objects.create(cid=self.club,event_name="Event",start_time="00:00:00",end_time="23:59:59",event_location="Library",event_description="Lots of testing!")

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get_or_create(first_name='testuser')[0])
        response = self.client.get(reverse('suite:club_view',kwargs={'club_id':self.club.pk}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Cool club")
        self.assertContains(response, "Lots of testing!")

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:club_view',kwargs={'club_id':self.club.pk}))
        self.assertRedirects(response, "/?next="+reverse('suite:club_view',kwargs={'club_id':self.club.pk}), 302,200)

    def test_get_login_multiple_events(self):
        event1 = Event.objects.create(cid=self.club,event_name="Event1",start_time="00:00:00",end_time="23:59:59",event_location="Library",event_description="Fun times!")

        event2 = Event.objects.create(cid=self.club,event_name="Event2",start_time="00:00:00",end_time="23:59:59",event_location="Library",event_description="Swag")

        self.client.force_login(get_user_model().objects.get_or_create(first_name='testuser')[0])
        response = self.client.get(reverse('suite:club_view',kwargs={'club_id':self.club.pk}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Cool club")
        self.assertContains(response, "Lots of testing!")
        self.assertContains(response, "Fun times!")
        self.assertContains(response, "Swag")

