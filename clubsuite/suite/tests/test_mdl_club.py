from django.test import TestCase
from suite.models import Club
from suite.models import ClubManager
from django.contrib.auth import get_user_model

#Testing ClubManager
class ClubManagerTestCase(TestCase):

    def setUp(self):

        # Assuming _create_permissions, _set_owner, and add_member works

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #Create club2
        self.club2=Club.objects.create(club_name="club2",club_type="PUB",club_description="another club")
        self.club2._create_permissions()
        self.club2._set_owner(self.owner)

        #Create private club
        self.club3=Club.objects.create(club_name="club3",club_type="PRI",club_description="private club")

        self.clubmanager=ClubManager()
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
            self.user_list.append(user)

    def test_qry_searchoneclub(self):
        club=self.clubmanager.qry_searchoneclub(self.club2.pk)
        self.assertEqual(club,self.club2)

    def test_qry_searchclubs_private(self):
        clubs=self.clubmanager.qry_searchclubs("private")
        self.assertEqual(len(clubs),0)

    def test_qry_searchclubs(self):
        clubs = self.clubmanager.qry_searchclubs("club")
        self.assertEqual(len(clubs),2)


#Testing mdl_club
class ClubTestCase(TestCase):
    def setUp(self):
        # Assuming _create_permissions, _set_owner, and add_member works

        #create club owner
        self.owner=get_user_model().objects.create(first_name="Owner",last_name="McPerson",email="test@test.com")
        self.owner.set_password("clubsuite")
        self.owner.save()


        #Create club
        self.club_description = ""
        for i in range(0,100):
            self.club_description += "a"
        self.club_description += "bbbbb"

        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description=self.club_description)
        self.club._create_permissions()
        self.club._set_owner(self.owner)

        #create a list to store club members
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

        # Create an actor with no permissions
        self.actor=get_user_model().objects.create(first_name="User",last_name="McPerson",email="test@testing.com")
        self.actor.set_password("clubsuite")
        self.actor.save()
        #create a user with no permissions
        self.user=get_user_model().objects.create(first_name="Person",last_name="McPerson",email="test@testing2.com")
        self.user.set_password("clubsuite")
        self.user.save()

    '''After setup, there will be 1 club with 1 owner, 19 members and also, 2 users'''
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

    def test_get_owners(self):
        owners=self.club.get_owners()
        self.assertEqual(owners[0],self.owner)

    def test_get_offficers(self):
        officers=self.club.get_officers()
        self.assertEqual(len(officers),1)

    def test_get_members(self):
        members=self.club.get_members()
        for i in range(0,20):
            self.assertEqual(members[i],self.user_list[i])

    def test_is_owner(self):
        self.assertTrue(self.club.is_owner(self.owner))
        for i in range(1,20):
            self.assertFalse(self.club.is_owner(self.user_list[i]))

    def test_is_officer(self):
        self.assertTrue(self.club.is_officer(self.owner))
        for i in range(1,20):
            self.assertFalse(self.club.is_officer(self.user_list[i]))

    def test_is_member(self):
        for i in range(0,20):
            self.assertTrue(self.club.is_member(self.user_list[i]))

    def test_get_group(self):
        self.assertEqual(self.club.get_group(self.owner),"Owner")
        for i in range(1,20):
            self.assertEqual(self.club.get_group(self.user_list[i]),"Member")

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

    def test_demote_from_officer(self):
        #Promote members to officer first
        for i in range(1,20):
            self.assertTrue(self.club.promote_to_officer(self.owner,self.user_list[i]))

        #Then demote them
        for i in range(1,20):
            self.assertTrue(self.club.demote_from_officer(self.owner,self.user_list[i]))

    def test_demote_from_officer_no_permission(self):
        #Promote 1 member
        self.assertTrue(self.club.promote_to_officer(self.owner,self.user_list[1]))
        self.assertFalse(self.club.demote_from_officer(self.actor,self.user_list[1]))

    def test_promote_officer_to_owner(self):
        #Promote members to officer first
        for i in range(1,20):
            self.assertTrue(self.club.promote_to_officer(self.owner,self.user_list[i]))

        #Then promote again
        for i in range(1,20):
            self.assertTrue(self.club.promote_officer_to_owner(self.owner,self.user_list[i]))

    def test_demote_owner_to_officer(self):
        #Promote members to officer first
        for i in range(1,20):
            self.assertTrue(self.club.promote_to_officer(self.owner,self.user_list[i]))

        #Then promote again
        for i in range(1,20):
            self.assertTrue(self.club.promote_officer_to_owner(self.owner,self.user_list[i]))

        #Finally, demote them
        for i in range(1,20):
            self.assertTrue(self.club.demote_owner_to_officer(self.owner,self.user_list[i]))
