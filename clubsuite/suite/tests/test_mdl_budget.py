from django.test import TestCase
from suite.models import Club
from suite.models import Budget
from suite.models import Division
from django.contrib.auth import get_user_model

class BudgetTestCase(TestCase):

    def setUp(self):

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")

        self.division = Division.objects.create(name="Division",cid=self.club)

    def test_valid_budget(self):
        #budget = Budget.objects.create(did=self.division,planned=1000,start_date="03/03/2027",end_date="03/04/2027")
        budget = Budget.objects.create(did=self.division,planned=1000,start_date="2027-03-03",end_date="2027-03-04")

        self.assertEqual(budget.did,self.division)
        self.assertEqual(budget.planned,1000)
        self.assertEqual(budget.start_date,"2027-03-03")
        self.assertEqual(budget.end_date,"2027-03-04")

    def test_str(self):
        #budget = Budget.objects.create(did=self.division,planned=1000,start_date="03/03/2027",end_date="03/04/2027")
        budget = Budget.objects.create(did=self.division,planned=1000,start_date="2027-03-03",end_date="2027-03-04")
        self.assertEqual(budget.__str__(),"Division and Plan: Division 1000")
