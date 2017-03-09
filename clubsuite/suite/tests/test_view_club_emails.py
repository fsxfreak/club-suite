from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import ClubEmails
from django.urls import reverse
from suite.models import Club

class View_ClubEmails_TestCase(TestCase):

    def setUp(self):
        self.client = Client()

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        self.user_list=[]
        self.user_list.append(self.owner)

        #add 19 users to club
        for i in range(1,20):
            #create users
            user=get_user_model().objects.create(first_name="Person"+str(i),last_name="McPerson",email="test"+str(i)+"@test.com")
            user.set_password("clubsuite")
            user.save()

            # add user to club
            self.club.add_member(self.owner,user)
            if (i%5 == 0):
                self.club.promote_to_officer(self.owner,user)
            self.user_list.append(user)

        self.club._set_owner(self.user_list[1])

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        response = self.client.get(reverse('suite:club_emails',kwargs={'club_id':self.club.id}),club_id=self.club.pk)
        self.assertEqual(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:club_emails',kwargs={'club_id':self.club.id}),club_id=self.club.pk)
        self.assertEqual(response.status_code,403)

    def test_post(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))

        #test member filter
        response = self.client.post(reverse('suite:club_emails',kwargs={'club_id':self.club.id}),club_id=self.club.pk,data={'member_type':"Member"},follow=True)

        self.assertEqual(response.status_code,200)
        for i in range(2,20):
            if ( i%5 != 0):
                self.assertContains(response, self.user_list[i].email)

        #test officer
        response = self.client.post(reverse('suite:club_emails',kwargs={'club_id':self.club.id}),club_id=self.club.pk,data={'member_type':"Officer"},follow=True)
        self.assertContains(response, self.user_list[5].email)
        self.assertContains(response, self.user_list[10].email)
        self.assertContains(response, self.user_list[15].email)

        #test owner
        response = self.client.post(reverse('suite:club_emails',kwargs={'club_id':self.club.id}),club_id=self.club.pk,data={'member_type':"Owner"},follow=True)
        self.assertNotContains(response, self.user_list[0].email)
        self.assertContains(response, self.user_list[1].email)
