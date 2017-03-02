from django.test import TestCase
from suite.models import Club
from suite.models import ClubManager
from django.contrib.auth import get_user_model

class ClubMemberQueryTestCase(TestCase):
    def setUp(self):

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()


        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #Create club2
        self.club2=Club.objects.create(club_name="club2",club_type="PUB",
                                    club_description="another club")
        self.club2._create_permissions()
        self.club2._set_owner(self.owner)

        #Create empty club
        self.club3=Club.objects.create(club_name="club3",club_type="PUB",club_description="empty club")


        self.clubmanager=ClubManager()
        self.user_list=[]

        #add users to club
        for i in range(1,20):
            #create users
            user=get_user_model().objects.create(first_name="Person"+str(i),last_name="McPerson",email="test"+str(i)+"@test.com")
            user.set_password("clubsuite")
            user.save()

            # add user to club
            self.club.add_member(self.owner,user)
            self.user_list.append(user)

    def test_club_roster(self):
        club_members=self.clubmanager.club_roster("club")
        self.assertEqual(club_members[0].first_name,self.ownerfirst_name)
        for i in range(1,20):
            self.assertEqual(club_members[i].first_name,self.user_list[i].first_name)


