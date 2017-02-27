from django.test import TestCase
from suite.models import Role
from suite.models import Club
from suite.forms import RegistrationForm
from suite.models import RoleManager

class ClubMemberQueryTestCase(TestCase):
    def setUp(self):

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.club2=Club.objects.create(club_name="club2",club_type="PUB",
                                    club_description="another club")
        self.club3=Club.objects.create(club_name="club3",club_type="PUB",
                                    club_description="empty club")
        self.rolemanager=RoleManager
       #Create members
        self.role_array=[]
        self.role_array2=[]
        for i in range(0,20):
            form=RegistrationForm(data={'email':"test"+str(i)+"@test.com",
                                        'password1':"clubsuite",
                                        'password2':"clubsuite",
                                        'first_name':"Person",
                                        'last_name':"McPerson"})
            self.assertTrue(form.is_valid())
            user=form.save()
            user.save()


            if i%2==1:
                #Create role
                role=Role.objects.create(cid=self.club,uid=user,title="member")
                self.role_array.append(role)
            else:
                #Create role
                role=Role.objects.create(cid=self.club2,uid=user,title="member")
                self.role_array2.append(role)


    def test_club_member_qry(self):
        club_members=self.rolemanager.qry_clubmembers(self.club)
        self.assertEqual(club_members[0].cid,self.role_array[0].cid)
        self.assertEqual(club_members[0].uid,self.role_array[0].uid)

    def test_multiple_club_member_qry(self):
        club_members=self.rolemanager.qry_clubmembers(self.club)
        for i in range(0,10):
            self.assertEqual(club_members[i].cid,self.role_array[i].cid)
            self.assertEqual(club_members[i].uid,self.role_array[i].uid)

    def test_not_in_club(self):
        club_members=self.rolemanager.qry_clubmembers(self.club3)
        self.assertEqual(len(club_members),0)

    def test_multiple_clubs(self):
        club_members=self.rolemanager.qry_clubmembers(self.club)
        for i in range(0,10):
            self.assertEqual(club_members[i].cid,self.role_array[i].cid)
            self.assertEqual(club_members[i].uid,self.role_array[i].uid)

        club_members2=self.rolemanager.qry_clubmembers(self.club2)
        for i in range(0,10):
            self.assertEqual(club_members2[i].cid,self.role_array2[i].cid)
            self.assertEqual(club_members2[i].uid,self.role_array2[i].uid)


