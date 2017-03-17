from django.test import TestCase
from suite.forms import RegistrationForm,ClubCreateForm,EventCreateForm,EditProfileForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import Client
from suite.models import Club,Division,User

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
        self.assertFalse(form.is_valid())

class EventCreateFormTestCase(TestCase):
    def setUp(self):
        #Create club
        self.club=Club.objects.create(club_name="club",club_type="PUB",club_description="a club")
        #Create division
        self.division=Division.objects.create(name="Expenses",cid=self.club)

    def test_valid_data(self):
        #IMPORTANT: start/end date cannot be in the past
        data = {
                'start_date':"03/05/2027",
                'end_date':"03/06/2027",
                'event_name':"Event",
                'start_time':"00:00:00",
                'end_time':"23:59:59",
                'event_location':"Library",
                'event_description':"So much fun",
                'event_cost':100,
                'event_fee':100,
                'accessibility':True,
                'required':False,
                'did':self.division.pk
                }

        form = EventCreateForm(data)
        if not form.is_valid():
            print(form.errors)

        event=form.save(self.club)

        self.assertTrue(event.event_name,"Event")

    def test_invalid_data(self):
        form = EventCreateForm(data={'event_name':"club event",
                                    'event_cost':100
                                    })
        self.assertFalse(form.is_valid())

class EditProfileFormTestCase(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create(email="test@test.com",first_name="User",last_name="Last")

    def test_valid_data(self):
        data={'email':"test2@test.com",'first_name':"NameChange",'last_name':"Change"}
        form=EditProfileForm(data,instance=self.user)
        if not form.is_valid():
            print(form.errors)

        user2=form.save()
        self.assertEqual(len(User.objects.all()),2)
        self.assertEqual(self.user,user2)
        self.assertEqual(self.user.first_name,"NameChange")
