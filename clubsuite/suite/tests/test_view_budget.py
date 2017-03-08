from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubCreate
from django.urls import reverse
from suite.models import Budget, Division, Club

class View_Budget_TestCase(TestCase):
    def setUp(self):
        self.client = Client()
        #client needs to be logged in

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)


    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        response = self.client.get(reverse('suite:budget',kwargs={'club_id':self.club.id}),club_id=self.club.pk)
        self.assertEqual(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:budget',kwargs={'club_id':self.club.id}),club_id=self.club.pk)
        self.assertEqual(response.status_code,403)

    def test_post(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        data_division = {'name':"Expenses",
                         'division':"1"}
        response = self.client.post(reverse('suite:budget',kwargs={'club_id':self.club.id}),data_division,club_id=self.club.pk,follow=True)
        self.assertEqual(response.status_code,200)
        division = Division.objects.get(name="Expenses")

        data_budget = {'did':division.pk,'planned':1000,'start_date':"03/05/17",'end_date':"03/06/17",'budget':"1"}

        response = self.client.post(reverse('suite:budget',kwargs={'club_id':self.club.id}),data_budget, follow=True)

        self.assertEqual(len(Budget.objects.filter(did=division.pk)),1)
