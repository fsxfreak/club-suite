from django.test import TestCase
from suite.models import Club
from django.contrib.auth import get_user_model
from suite.views import Dashboard
from django.test import Client
from django.urls import reverse

class View_Dashboard_TestCase(TestCase):

    def setUp(self):

        self.client = Client()

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="Cool club",club_type="PUB",club_description="sick")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #Create club2
        self.club2=Club.objects.create(club_name="Lame",club_type="PUB",club_description="nice")
        self.club2._create_permissions()
        self.club2._set_owner(self.owner)

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))

        response = self.client.get(reverse('suite:dashboard'))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Cool club")
        self.assertContains(response,"Lame")
        self.assertContains(response,"sick")
        self.assertContains(response,"nice")

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:dashboard'))
        self.assertRedirects(response, "/?next="+reverse('suite:dashboard'), 302,200)

