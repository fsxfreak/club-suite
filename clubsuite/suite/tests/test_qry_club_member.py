from django.test import TestCase
from suite.models import Club
from suite.forms import RegistrationForm
from suite.models import ClubManager

class ClubMemberQueryTestCase(TestCase):
    def setUp(self):

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.club2=Club.objects.create(club_name="club2",club_type="PUB",
                                    club_description="another club")
        self.club3=Club.objects.create(club_name="club3",club_type="PUB",
                                    club_description="empty club")

        self.clubmanager=ClubManager
        self.user_list=[]
        for i in range(0,20):
            form=RegistrationForm(data={'email':"test"+str(i)+"@test.com",'password1':"clubsuite",'password2':"clubsuite",'first_name':"Person"+str(i),'last_name':"McPerson"})
            self.assertTrue(form.is_valid())
            user=form.save()
            user.join_the_club(self.club)
            self.user_list.append(user)

    def test_club_roster(self):
        club_members=self.clubmanager.club_roster("club")
        for i in range(0,20):
            self.assertEqual(club_members[i].first_name,self.user_list[i].first_name)
            self.assertEqual(club_members[i].first_name,self.user_list[i].first_name)


