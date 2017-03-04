from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubJoin
from suite.models import Club, JoinRequest
from django.urls import reverse

class View_Club_Join_TestCase(TestCase):
    def setUp(self):
        self.client=Client()
        self.club=Club.objects.create(club_name="club",club_type="PUB", club_description="a club")

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()


    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get_or_create(first_name='testuser')[0])
        response = self.client.get(reverse('suite:club_join',kwargs={'club_id':self.club.id}))
        self.assertEquals(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:club_join',kwargs={'club_id':self.club.id}))
        self.assertRedirects(response,"/?next="+reverse('suite:club_join',kwargs={'club_id':self.club.id}))

    #TODO Check JoinRequest after class is finished
    def test_post(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))

        data = {"reason":"please",
                "club_id":self.club.pk}
        data2 = {"reason":"cmon",
                "club_id":self.club.pk}
        data3 = {"reason":"ayo",
                "club_id":self.club.pk}

        response = self.client.post(reverse('suite:club_join',kwargs={'club_id':self.club.id}),data)

        self.assertRedirects(response,reverse('suite:club_view',kwargs={'club_id':self.club.id}))

        response2 = self.client.post(reverse('suite:club_join',kwargs={'club_id':self.club.id}),data2)

        response3 = self.client.post(reverse('suite:club_join',kwargs={'club_id':self.club.id}),data3)

        requests=JoinRequest.objects.filter(cid=self.club.pk).filter(uid=self.owner.pk)

        self.assertEqual(len(requests),1)
