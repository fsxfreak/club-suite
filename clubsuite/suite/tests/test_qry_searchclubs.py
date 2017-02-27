from django.test import TestCase
from suite.models import Club
from suite.models import ClubManager


class ClubQueryTestCase(TestCase):
    def setUp(self):

        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",
                                    club_description="a club")
        self.club2=Club.objects.create(club_name="club2",club_type="PUB",
                                    club_description="another club")
        self.club3=Club.objects.create(club_name="club3",club_type="PUB",
                                    club_description="empty")
        self.club4=Club.objects.create(club_name="club4",club_type="PRI",
                                    club_description="private")
        self.clubmanager=ClubManager

    def test_search_one_club(self):
        clubs=self.clubmanager.qry_searchclubs("club2")
        self.assertNotEqual(len(clubs),0)
        '''
        for i in range(0,len(clubs)):
            print(clubs[i].club_name)#debug
        '''
        self.assertEqual(clubs[0],self.club2)

    def test_search_private_club(self):
        clubs=self.clubmanager.qry_searchclubs("private")
        self.assertEqual(len(clubs),0)

    def test_search_club_name(self):
        clubs = self.clubmanager.qry_searchclubs("club")
        self.assertEqual(len(clubs),3)
