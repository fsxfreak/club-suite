from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from guardian.shortcuts import remove_perm
from guardian.models import UserObjectPermission

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        user = self.model(
                email=self.normalize_email(email),
                is_active=True,
                **kwargs
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # TODO define needed fields

    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20,default="FirstName")
    last_name = models.CharField(max_length=20,default="LastName")

    # Do not specify permissions using boolean fields. Use PermissionsMixin.

    def get_full_name(self):
        return self.first_name+' '+self.last_name
    def get_short_name(self):
        return self.first_name
    def __str__(self):
        return self.first_name+' '+self.last_name
#helper function: check whether the user has certain permission for a club
#param: codename, club object
#return: True if have the permission, False for not
    def has_perm(self,i_codename,club_obj):
        return self.has_perm(i_codename,club_obj)

#helper function: add certain permission of a club to a user
#param: codename, club object
    def add_perm(self,i_codename,club_obj):
        UserObjectPermission.objects.assign_perm(i_codename,self,obj=club_obj)

    def remove_perm(self, i_codename, club_obj):
        remove_perm('M', self, club_obj)

#promote the user from member to officer in club club_obj
    def promote_to_officer(self, club_obj):
        self.add_perm(self, "A", club_obj)
        self.add_perm(self, 'can_handle_join_requests', club_obj)
        self.add_perm(self, 'can_handle_promotion_requests', club_obj)
        self.add_perm(self, 'can_view_stats', club_obj)
        self.add_perm(self, 'can_create_event', club_obj)
        self.add_perm(self, 'can_add_receipt', club_obj)
        self.add_perm(self, 'can_remove_receipt', club_obj)
        self.add_perm(self, 'can_access_attendance', club_obj)
        self.add_perm(self, 'can_access_budget', club_obj)
        self.add_perm(self, 'can_create_budget', club_obj)
        self.add_perm(self, 'can_request_reimbusement', club_obj)

        exist=Group.objects.filter(name=club_obj.club_name).count()
        if not exist==1:
            group = Group.objects.create(name=club_obj.club_name)
            self.groups.add(group)
        else:
            group = Group.objects.get(name=club_obj.club_name)
            self.groups.add(group)

#let the user join the club
    def join_the_club(self,club_obj):
        club_obj.members.add(self)
        self.add_perm(self, "M", club_obj)
        
        exist=Group.objects.filter(name=club_obj.club_name).count()
        if not exist==1:
            group = Group.objects.create(name=club_obj.club_name)
            self.groups.add(group)
        else:
            group = Group.objects.get(name=club_obj.club_name)
            self.groups.add(group)

    def leave_club(self, club_obj):
        club.members.remove(request.user)
        remove_perm('M', self, club_obj)

        group = Group.objects.get(name=club_obj.club_name)
        self.groups.remove(group)

#deny the user from joining the club
    def deny_the_user(self,club_obj):
        self.add_perm(self,"P", club_obj)

#get all clubs the user is in
    def get_clubs(self):        
        all_clubs = [x.name for x in self.groups.all()]
        return Club.objects.filter(club_name__in=all_clubs)

class Account(models.Model):
    user = models.OneToOneField(
       User, 
       on_delete = models.CASCADE,
       primary_key = True,
    )
    preferred_name = models.CharField(max_length=20, blank=True)

    UNDERGRAD = 'U'
    GRADUATE = 'G'
    OTHERS = 'O'
    S_T_CHOICES = (
      (UNDERGRAD, 'Undergraduate'),
      (GRADUATE, 'Graduate'),
      (OTHERS, 'Others'),
    )
    student_title = models.CharField(
      max_length=1, 
      choices=S_T_CHOICES, 
      default=OTHERS)
    graduation_year = models.IntegerField(default=0)
    major = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=50, blank=True)
    GPA = models.DecimalField(max_digits=4, decimal_places=3, default=0.000)

    def __str__(self):
        return str(self.user)  
