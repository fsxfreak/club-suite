from django.test import TestCase
from suite.models import UserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from suite.models import Club

class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(first_name="First",last_name="Last",email="test@test.com")
        self.user.set_password("testclub123")
        self.user.save()
        self.club=Club.objects.create('club_name':"club1",'club_type':"PUB",'club_description':"a club")


    def test_user(self):
        #reg_email=UserManager.objects.get(email)
        self.assertEqual(self.user.email,"test@test.com")
        self.assertEqual(self.user.get_short_name(),"First")
        self.assertEqual(self.user.get_full_name(),"First Last")
        self.assertEqual(self.user.last_name,"Last")
        self.assertTrue(check_password("testclub123",self.user.password))

    def test_join_the_club(self):
        self.user.join_the_club(self.club)
        self.assertTrue(self.user.has_perm("M",self.club))

    def test_promote_to_officer(self):
        self.user.join_the_club(self.club)
        self.assertTrue(self.user.has_perm("A",self.club))

    def test_deny_the_user(self):
        self.user.deny_the_user(self.club)
        self.assertTrue(self.user.has_perm("P",self.club))

    def test_get_clubs(self):
        self.club2=Club.objects.create('club_name':"club2",'club_type':"PUB",'club_description':"a club")
        self.user.join_the_club(self.club)
        self.user.join_the_club(self.club2)

        club_list=self.user.get_clubs()
        self.assertEqual(club_list[0],self.club)
        self.assertEqual(club_list[1],self.club2)



class UserManagerTestCase(TestCase):
    def setUp(self):
        self.usermanager=UserManager

    def test_create_user(self):
        user=self.usermanager.create_user("test@test.com","clubsuite")
        self.assertEqual(user.email,"test@test.com")
        self.assertTrue(check_password("clubsuite",user.password))

    def test_create_superuser(self):
        user=self.usermanager.create_user("test@test.com","clubsuite")
        self.assertEqual(user.email,"test@test.com")
        self.assertTrue(check_password("clubsuite",user.password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
