from django.test import TestCase
from suite.forms import RegistrationForm
from suite.forms import ClubCreateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import Client
# Create your tests here.
#

class RegistrationFormTestCase(TestCase):
    def setUp(self):
        pass

    def test_valid_data(self):
        form=RegistrationForm(data={'email':"test@test.com",
                                'password1':"clubsuite",
                                'password2':"clubsuite",
                                'first_name':"First",
                                'last_name':"Last"})
        user=form.save()

        self.assertTrue(form.is_valid())
        self.assertTrue(user.email=="test@test.com")
        self.assertTrue(check_password("clubsuite",user.password))
        self.assertTrue(user.first_name, "First")
        self.assertTrue(user.last_name, "Last")

    def test_invalid_data(self):
        form = RegistrationForm(data={'email':"club@club.com",
                                      'password1':"pass",
                                      'password2':"pass",
                                      'first_name':"First"
                                    })

        self.assertFalse(form.is_valid())

    def test_invalid_passwords(self):
        form = RegistrationForm(data={'email':"club@club.com",
                                      'password1':"pass",
                                      'password2':"pass2",
                                      'first_name':"First",
                                      'last_name':"Last"
                                    })

        self.assertFalse(form.is_valid())

class ClubCreateFormTestCase(TestCase):
    def setUp(self):
        pass
    def test_valid_data(self):
        form = ClubCreateForm(data={'club_name':"club",
                                    'club_type':"PUB",
                                    'club_description':"cool"})

        club=form.save()
        self.assertTrue(form.is_valid())
        self.assertTrue(club.club_name,"club")
        self.assertTrue(club.club_type,"PUB")
        self.assertTrue(club.club_description,"cool")

    def test_invalid_data(self):
        form = ClubCreateForm(data={'club_name':"club",
                                    'club_type':"PUB"
                                    })

        #club=form.save()
        self.assertFalse(form.is_valid())
        '''
        self.assertTrue(club.club_name,"club")
        self.assertTrue(club.club_type,"PUB")
        self.assertTrue(club.club_description,"cool")
        '''

