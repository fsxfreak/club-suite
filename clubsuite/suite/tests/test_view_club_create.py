from django.test import TestCase
from django.test import Client
from suite.views import ClubCreate
from django.urls import reverse

class View_Club_Create_TestCase(TestCase):
    def setUp(self):

        self.client = Client()

        #self.clubCreate = ClubCreate.objects.create()

    def test_get(self):
        response = self.client.get(reverse('suite:club_create'))
        #self.assertEqual(response.status_code,200)
        self.assertRedirects(response, reverse('suite:club_create'), 302,200)

    def test_post(self):
        data = {
                'club_name':"Club",
                'club_type':"PUB",
                'club_description':"Pretty cool"
                }
        response = self.client.post(reverse('suite:club_create'),data, follow=True)
        self.assertEqual(response.status_code,200)

#    def test_post_invalid(self):

