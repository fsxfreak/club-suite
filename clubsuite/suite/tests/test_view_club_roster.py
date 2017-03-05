from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubRoster
from django.urls import reverse
from suite.models import Club

class View_Club_Roster_TestCase(TestCase):
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

        #add users to club
        self.user_list=[]
        self.user_list.append(self.owner)

        for i in range(1,20):
            #create users
            user=get_user_model().objects.create(first_name="Person"+str(i),last_name="McPerson",email="test"+str(i)+"@test.com")
            user.set_password("clubsuite")
            user.save()

            # add user to club
            self.club.add_member(self.owner,user)
            self.user_list.append(user)


    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name="Owner"))
        response = self.client.get(reverse('suite:club_roster',kwargs={'club_id':self.club.id}),club_id=self.club.pk)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,self.club.club_name)
        self.assertContains(response,self.owner.first_name)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:club_roster',kwargs={'club_id':self.club.id}))
        self.assertRedirects(response, "/?next="+reverse('suite:club_roster',kwargs={'club_id':self.club.id}), 302,200)

    def test_post_delete(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        self.assertTrue(self.club.is_member(self.user_list[1]))
        self.assertTrue(self.club.is_owner(self.owner))
        data = {
                'delete':self.user_list[1].pk,
                'club_id':self.club.pk
                }
        response = self.client.post(reverse('suite:club_roster',kwargs={'club_id':self.club.id}),data,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertFalse(self.club.is_member(self.user_list[1]))

    def test_post_promote(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        data = {
                'promote':self.user_list[1].pk,
                'club_id':self.club.pk
                }
        response = self.client.post(reverse('suite:club_roster',kwargs={'club_id':self.club.id}),data,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue(self.club.is_officer(self.user_list[1]))
