from django.test import TestCase
from suite.models import Club
from suite.models import ClubManager
from django.contrib.auth import get_user_model

class ClubManagerTestCase(TestCase):

    def setUp(self):

        # Assuming _create_permissions and _set_owner work

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

        #Create private club
        self.club3=Club.objects.create(club_name="club3",club_type="PRI",club_description="private club")

        self.clubmanager=ClubManager()
        self.user_list=[]
        self.user_list.append(self.owner)

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

    def test_qry_searchoneclub(self):
        club=self.clubmanager.qry_searchoneclub(self.club2.pk)
        self.assertEqual(club,self.club2)

    def test_qry_searchclubs_private(self):
        clubs=self.clubmanager.qry_searchclubs("private")
        self.assertEqual(len(clubs),0)

    def test_qry_searchclubs(self):
        clubs = self.clubmanager.qry_searchclubs("club")
        self.assertEqual(len(clubs),2)

class ClubTestCase(TestCase):
    def setUp(self):
         #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        self.club_description = ""

        #Create club

        for i in range(0,100):
            self.club_description += "a"
        self.club_description += "bbbbb"

        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description=self.club_description)
        self.club._create_permissions()

        # Actor has no permissions
        self.actor=get_user_model().objects.create(first_name="User",last_name="McPerson",email="test@testing.com")
        self.actor.set_password("clubsuite")
        self.actor.save()

        self.user=get_user_model().objects.create(first_name="Person",last_name="McPerson",email="test@testing2.com")
        self.user.set_password("clubsuite")
        self.user.save()

        self.club._set_owner(self.owner)
        self.user_list=[]
        self.user_list.append(self.owner)

        #add users to club
        for i in range(1,20):
            #create users
            user=get_user_model().objects.create(first_name="Person"+str(i),last_name="McPerson",email="test"+str(i)+"@test.com")
            user.set_password("clubsuite")
            user.save()

            # add user to club
            self.club.add_member(self.owner,user)
            self.user_list.append(user)

    def test__str__(self):
        self.assertEqual(self.club.__str__(),"club")

    def test_summary(self):
        self.assertEqual(self.club.summary(),self.club_description[:100])

    def test_get_owner_group_name(self):
        self.assertEqual(self.club._get_owner_group_name(),"club_owners")

    def test_get_officer_group_name(self):
        self.assertEqual(self.club._get_officer_group_name(),"club_officers")

    def test_get_member_group_name(self):
        self.assertEqual(self.club._get_member_group_name(),"club_members")

    def test_add_member_no_permission(self):

        self.assertFalse(self.club.add_member(self.actor,self.user))

    def test_remove_member_permission(self):

        for i in range(1,20):
            self.assertTrue(self.club.remove_member(self.owner,self.user_list[i]))

    def test_remove_member_no_permission(self):
        self.assertFalse(self.club.remove_member(self.actor,self.user_list[1]))

    def test_promote_to_officer_no_permission(self):
        self.assertFalse(self.club.promote_to_officer(self.actor,self.user_list[1]))

    def test_promote_to_officer_permission(self):
        for i in range(1,20):
            self.assertTrue(self.club.promote_to_officer(self.owner,self.user_list[i]))

    #TODO test_demote_from_officer

