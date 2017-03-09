from django.test import TestCase
from suite.models import Club
from suite.models import Budget
from suite.models import Division
from django.contrib.auth import get_user_model

class DivisionTestCase(TestCase):

    def setUp(self):

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")


    def test_valid_division(self):

        division = Division.objects.create(name="Division",cid=self.club)

        self.assertEqual(division.cid,self.club)
        self.assertEqual(division.name,"Division")

    def test_str(self):
        division = Division.objects.create(name="Division",cid=self.club)
        self.assertEqual(division.__str__(),"Division")
