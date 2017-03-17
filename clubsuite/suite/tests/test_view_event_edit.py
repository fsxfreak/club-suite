from django.test import TestCase, RequestFactory
from django.test import Client
from suite.views import EventEdit
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from suite.models import Club,Event,Division
from django.contrib.messages.storage.fallback import FallbackStorage

class ViewEventEditTestCase(TestCase):
    def setUp(self):
        self.client=Client()
        self.request_factory=RequestFactory()

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #create division
        self.division=Division.objects.create(name="Expenses",cid=self.club)

        #create event
        self.event = Event.objects.create(cid=self.club,event_name="Event1",start_date="2020-03-29",start_time="00:00:00",end_date="2020-03-29",end_time="23:59:59",event_location="Library",event_description="Lots of testing!",event_cost=1000,event_fee=10,accessibility=False,required=True,did=self.division)



    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        response = self.client.get(reverse('suite:event_edit',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}))
        self.assertEquals(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:event_edit',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}))
        self.assertEquals(response.status_code,403)

    def test_post(self):
        #login
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))

        data = {
                'edit':"1",
                'start_date':"03/05/2027",
                'end_date':"03/06/2027",
                'event_name':"Event",
                'start_time':"00:00:00",
                'end_time':"23:59:59",
                'event_location':"Library",
                'event_description':"So much fun",
                'event_cost':100,
                'event_fee':100,
                'accessibility':True,
                'required':False,
                'did':self.division.pk
                }

        request=self.request_factory.post(reverse('suite:event_edit',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}),data,follow=True)
        request.user=self.owner
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response=EventEdit.as_view()(request,club_id=self.club.pk,event_id=self.event.pk)
        response.client=self.client

        #Assert that it redirects to club manage page
        self.assertRedirects(response,reverse('suite:club_view',kwargs={'club_id':self.club.pk}))

        #self.event's strings are still pointing to old information, need get() to refresh
        newEvent=Event.objects.get(event_name="Event")
        self.assertEqual(newEvent,self.event)
        self.assertEqual(newEvent.event_name, "Event")
        self.assertEqual(newEvent.event_description, "So much fun")

