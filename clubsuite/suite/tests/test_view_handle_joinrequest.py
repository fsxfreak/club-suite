from suite.models import JoinRequest
from django.test import TestCase
from suite.models import Club
from django.contrib.auth import get_user_model
from suite.views import HandleJoinRequest
from django.test import Client
from django.urls import reverse

class View_Handle_Join_Request_TestCase(TestCase):

    def setUp(self):
        self.client=Client()
        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #Create user
        self.user=get_user_model().objects.create(first_name="User",last_name="McGuy",email="test2@test.com")
        self.user.set_password("clubsuite")
        self.user.save()

        #Create user2
        self.user2=get_user_model().objects.create(first_name="User2",last_name="McGuy",email="test3@test.com")
        self.user2.set_password("clubsuite")
        self.user2.save()

        #Create user3
        self.user3=get_user_model().objects.create(first_name="User3",last_name="McGuy",email="test4@test.com")
        self.user3.set_password("clubsuite")
        self.user3.save()


        self.joinRequest=JoinRequest.objects.create(cid=self.club,uid=self.user,reason="Please")
        self.joinRequest2=JoinRequest.objects.create(cid=self.club,uid=self.user2,reason="cmon")
        self.joinRequest3=JoinRequest.objects.create(cid=self.club,uid=self.user3,reason="help me out")

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        response = self.client.get(reverse('suite:handle_join_request',kwargs={'club_id':self.club.id}))
        self.assertEquals(response.status_code,200)

    def test_post(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        data = {"accept":self.joinRequest.pk}
        response = self.client.post(reverse('suite:handle_join_request',kwargs={'club_id':self.club.id}),data)
        self.assertNotContains(response,"Please")
        self.assertContains(response,"cmon")
        self.assertContains(response,"help me out")
