from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import EventCreate
from django.urls import reverse
from suite.models import Club

class View_EventCreate_TestCase(TestCase):
    def setUp(self):
        self.client = Client()

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #self.event = Event.objects.create(cid=self.club,event_name="Event1",start_time="00:00:00",end_time="23:59:59",event_location="Library",event_description="Lots of testing!")

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        response = self.client.get(reverse('suite:event_create',kwargs={'club_id':self.club.pk}))
        self.assertEqual(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:event_create',kwargs={'club_id':self.club.pk}))
        #self.assertRedirects(response, "/?next="+reverse('suite:event_create',kwargs={'club_id':self.club.pk}), 403,200)
        self.assertEquals(response.status_code,403)

    def test_post(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        data = {
                'start_date':"03/05/2017",
                'end_date':"03/06/2017",
                'cid':self.club.pk,
                'event_name':"Event",
                'start_time':"00:00:00",
                'end_time':"23:59:59",
                'event_location':"Library",
                'event_description':"So much fun",
                'event_cost':100,
                'accessibility':True,
                'required':False
                }
        response = self.client.post(reverse('suite:event_create',kwargs={'club_id':self.club.pk}),data, follow=True)
        self.assertRedirects(response,reverse('suite:club_view',kwargs={'club_id':self.club.pk}))

        self.assertContains(response, "Event")
