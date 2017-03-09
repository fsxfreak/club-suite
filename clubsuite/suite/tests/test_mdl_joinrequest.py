from django.test import TestCase
from suite.models import Club
from django.contrib.auth import get_user_model
from suite.models import JoinRequest

class JoinRequestTestCase(TestCase):

    def setUp(self):

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

    def test_valid_JoinRequest(self):
        joinRequest = JoinRequest.objects.create(cid=self.club,uid=self.owner,reason="Please")

        self.assertEqual(joinRequest.cid,self.club)
        self.assertEqual(joinRequest.uid,self.owner)
        self.assertEqual(joinRequest.reason,"Please")

    def test_str(self):
        joinRequest = JoinRequest.objects.create(cid=self.club,uid=self.owner,reason="Please")

        self.assertEqual(joinRequest.__str__(),"JoinRequest: Owner McPerson wants to join club because Please")
