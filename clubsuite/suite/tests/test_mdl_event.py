from django.test import TestCase
from suite.models import EventManager, Event
from suite.models import Club
from django.contrib.auth import get_user_model
from datetime import datetime

class EventTestCase(TestCase):

    def setUp(self):

        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")


        self.eventManager = EventManager()
        self.event = Event.objects.create(cid=self.club,event_name="Event1",start_time="00:00:00",end_time="23:59:59",event_location="Library",event_description="Lots of testing!")

    def test_get_upcoming_events(self):
       event_list = self.eventManager.get_upcoming_events(self.club.pk)
       self.assertEqual(self.event,event_list[0])
