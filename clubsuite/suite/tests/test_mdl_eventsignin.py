from django.test import TestCase
from suite.models import EventSignInManager, EventSignIn
from suite.models import Event
from suite.models import Club
from django.contrib.auth import get_user_model

class EventSignInTestCase(TestCase):
    def setUp(self):
        #Create club and user
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.user=get_user_model().objects.create(first_name="Person",last_name="McPerson",email="test@test.com")
        self.user.set_password("clubsuite")
        self.user.save()

        #Create event
        self.eventSignInManager = EventSignInManager()
        self.event = Event.objects.create(cid=self.club,event_name="Event1",start_time="00:00:00",end_time="23:59:59",event_location="Library",event_description="Lots of testing!")
        self.eventSignIn=EventSignIn.objects.create(cid=self.club,eid=self.event,uid=self.user)

    def test__str__(self):
        self.assertEqual(self.eventSignIn.__str__(),"User " + self.user.get_full_name() + " Event " + self.event.event_name + " Club " + self.club.club_name)

    def test_get_attended_events(self):
        event_list = self.eventSignInManager.get_attended_events(self.user,self.club)
        self.assertEqual(event_list[0],self.event)

    def test_get_all_attended_events(self):
        event_list = self.eventSignInManager.get_all_attended_events(self.user)
        self.assertEqual(event_list[0],self.event)
