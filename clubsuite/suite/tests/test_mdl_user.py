from django.test import TestCase
from suite.models import UserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from suite.models import Club

class UserTestCase(TestCase):
    def setUp(self):
        #create user
        self.user = get_user_model().objects.create(first_name="First",last_name="Last",email="test@test.com")
        self.user.set_password("testclub123")
        self.user.save()

        #create club
        self.club=Club.objects.create(club_name="club1",club_type="PUB",club_description="a club")
        self.club._create_permissions()

        self.owner = get_user_model().objects.create(first_name="Officer",last_name="Last",email="test0@test123.com")
        self.owner.set_password("testclub123")
        self.owner.save()

        self.club._set_owner(self.owner)

    def test_user(self):
        self.assertEqual(self.user.email,"test@test.com")
        self.assertEqual(self.user.get_short_name(),"First")
        self.assertEqual(self.user.get_full_name(),"First Last")
        self.assertEqual(self.user.last_name,"Last")
        self.assertTrue(check_password("testclub123",self.user.password))

    def test_get_clubs(self):
        #create club2
        club2=Club.objects.create(club_name="club2",club_type="PUB",club_description="a club")
        club2._create_permissions()

        club2._set_owner(self.owner)

        #add user to both clubs
        self.club.add_member(self.owner,self.user)
        club2.add_member(self.owner,self.user)

        #test get clubs
        #NOTE fails because add_member method doesn't work
        club_list=self.user.get_clubs()
        self.assertEqual(club_list[0],self.club)
        self.assertEqual(club_list[1],club2)

    def test_get_clubs(self):

        #create club
        club2=Club.objects.create(club_name="club2",club_type="PUB",club_description="something")
        club2._create_permissions()
        club2._set_owner(self.owner)

        self.assertEqual(len(self.owner.get_clubs()),2)
