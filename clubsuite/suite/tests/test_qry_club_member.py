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
        self.club3=Club.objects.create(club_name="club3",club_type="PUB",club_description="empty club")

        #create club owner
        form=RegistrationForm(data={'email':"test@test.com",'password1':"clubsuite",'password2':"clubsuite",'first_name':"Owner",'last_name':"McPerson"})
        self.assertTrue(form.is_valid())
        self.owner=form.save()
        self.owner.save()
        self.club._set_owner(self.owner)


        self.clubmanager=ClubManager
        self.user_list=[]

        #add users to club
        for i in range(1,20):
            form=RegistrationForm(data={'email':"test"+str(i)+"@test.com",'password1':"clubsuite",'password2':"clubsuite",'first_name':"Person"+str(i),'last_name':"McPerson"})
            self.assertTrue(form.is_valid())
            user=form.save()
            user.save()
            self.club.add_member(self.owner,user)
            self.user_list.append(user)

    def test_club_roster(self):
        club_members=self.clubmanager.club_roster("club")
        self.assertEqual(club_members[0].first_name,self.ownerfirst_name)
        for i in range(1,20):
            self.assertEqual(club_members[i].first_name,self.user_list[i].first_name)


