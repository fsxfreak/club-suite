from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from suite.views import Event
from django.urls import reverse
from suite.models import Club,Division
from suite.models import Event

class View_Event_TestCase(TestCase):
    def setUp(self):
        self.client = Client()

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #create division
        division=Division.objects.create(name="Expenses",cid=self.club)
        self.event = Event.objects.create(start_date="2027-03-05",
            end_date="2027-03-06",
            cid=self.club,
            event_name="Event",
            start_time="00:00:00",
            end_time="23:59:59",
            event_location="Library",
            event_description="So much fun",
            event_cost=100,
            event_fee=100,
            accessibility=True,
            required=False,
            did=division)

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))

        response = self.client.get(reverse('suite:event',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}),club_id=self.club,event_id=self.event)
        self.assertEqual(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:event',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}),club_id=self.club,event_id=self.event,follow=True)
        self.assertEquals(response.status_code,200)


    def test_post(self):
        #login
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        data = {'going':self.owner.pk}
        response = self.client.post(reverse('suite:event',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}),data,club_id=self.club,event_id=self.event, follow=True)
        #Assert that it redirects to club page
        self.assertRedirects(response,reverse('suite:event',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}))

        self.assertContains(response, "Total Members who Signed In: 1")

    def test_post_revenue(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        data = {'going':self.owner.pk}
        response = self.client.post(reverse('suite:event',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}),data,club_id=self.club,event_id=self.event, follow=True)
        #Assert that it redirects to club page
        self.assertRedirects(response,reverse('suite:event',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}))

        user_list=[]
        user_list.append(self.owner)

        #add 19 users to club
        for i in range(1,20):
            #create users
            user=get_user_model().objects.create(first_name="Person"+str(i),last_name="McPerson",email="test"+str(i)+"@test.com")
            user.set_password("clubsuite")
            user.save()

            # add user to club
            self.club.add_member(self.owner,user)
            user_list.append(user)

            data = {'going':user_list[i].pk}
            response = self.client.post(reverse('suite:event',kwargs={'club_id':self.club.pk,'event_id':self.event.pk}),data,club_id=self.club,event_id=self.event, follow=True)


            self.assertContains(response, "Total Members who Signed In: "+ str(i+1))

        self.assertContains(response, "Total Revenue: 2000")






