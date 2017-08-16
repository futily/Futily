from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ['preferred_platforn']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)

    about_me = models.TextField(blank=True, null=True)

    preferred_platform = models.CharField(max_length=255, choices=[
        ('psn', 'Playstation'),
        ('xbox', 'xBox'),
        ('origin', 'PC'),
    ], default='psn')

    psn = models.CharField(max_length=255, blank=True, null=True)
    xbox = models.CharField(max_length=255, blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)

    twitter = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    twitch = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)

    favourite_player = models.ForeignKey('players.Player', blank=True, null=True)
    favourite_club = models.ForeignKey('clubs.Club', blank=True, null=True)
    favourite_nation = models.ForeignKey('nations.Nation', blank=True, null=True)

    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={
            'username': self.username
        })

    def get_collection_url(self):
        return self.get_absolute_url()

    def get_profile_url(self):
        return self.get_absolute_url()

    def get_packs_url(self):
        return reverse('users:packs', kwargs={
            'username': self.username
        })

    def get_settings_url(self):
        return reverse('users:settings', kwargs={
            'username': self.username
        })

    def get_squads_url(self):
        return self.get_absolute_url()

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def get_short_name(self):
        return self.get_username()

    def get_full_name(self):
        return self.get_username()
