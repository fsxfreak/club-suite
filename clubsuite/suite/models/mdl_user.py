from django.db import models
<<<<<<< HEAD
=======
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

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
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # TODO define needed fields

    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    # Do not specify permissions using boolean fields. Use PermissionsMixin.

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email


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
>>>>>>> 8803458abcee1487920c03a6f3c50cf61883dcc0