from django.test import TestCase, RequestFactory
from django.test import Client
from suite.views import ClubEdit
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from suite.models import Club

class ViewClubEditTestCase(TestCase):
    def setUp(self):
        self.client=Client()
        self.request_factory=RequestFactory()

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()
        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

    def test_get_login(self):
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))
        response = self.client.get(reverse('suite:club_edit',kwargs={'club_id':self.club.pk}))
        self.assertEquals(response.status_code,200)

    def test_get_not_logged_in(self):
        response = self.client.get(reverse('suite:club_edit',kwargs={'club_id':self.club.pk}))
        self.assertEquals(response.status_code,403)

    def test_post(self):
        #login
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))

        data={'edit':'1','club_name':"newClub",'club_description':"newest club",'instance':self.club}

        request=self.request_factory.post(reverse('suite:club_edit',kwargs={'club_id':self.club.pk}),data)
        request.user=self.owner
        response=ClubEdit.as_view()(request,club_id=self.club.pk)
        response.client=self.client

        '''
        response = self.client.post(reverse('suite:club_edit',kwargs={'club_id':self.club.pk}),data,club_id=self.club.pk,follow=True)
        '''
        #Assert that it redirects to club manage page
        self.assertRedirects(response,reverse('suite:club_manage'))

        self.assertEqual(self.club.club_name, "newClub")
        self.assertEqual(self.club.club_type, "PRI")
        self.assertEqual(self.club.club_description, "newest club")

    def test_post_invalid(self):
        club2=Club.objects.create(club_name="club2",club_type="PUB",club_description="club #2")
        club2._create_permissions()
        club2._set_owner(self.owner)

        #login
        self.client.force_login(get_user_model().objects.get(first_name='Owner'))

        #post should be invalid because edited club to have same name as club2
        data={'edit':'1','club_name':"club2",'club_description':"newest club"}
        response = self.client.post(reverse('suite:club_edit',kwargs={'club_id':self.club.pk}),data,club_id=self.club.pk,follow=True)

        self.assertEquals(response.status_code,200)
