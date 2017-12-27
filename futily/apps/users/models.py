from annoying.fields import AutoOneToOneField
from cms import sitemaps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse

from futily.apps.actions.utils import create_action


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

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ['preferred_platform']
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

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

    followers = models.ManyToManyField('self', symmetrical=False, through='users.UserFollowers',
                                       related_name='following')

    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def get_followers(self):
        return self.followers.filter(to_user__from_user=self)

    @property
    def get_following(self):
        return self.following.filter(from_user__to_user=self)

    def is_following(self, user):
        return user.get_followers.filter(id=self.id).exists()

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={
            'username': self.username
        })

    def get_collection_url(self):
        return reverse('users:collection', kwargs={
            'username': self.username
        })

    def get_favourite_players_url(self):
        return reverse('users:favourite-players', kwargs={
            'username': self.username
        })

    def get_collection_club_url(self, league, club):
        return reverse('users:collection-club', kwargs={
            'username': self.username,
            'league_slug': league.slug,
            'club_slug': club.slug,
        })

    def get_collection_league_url(self, league):
        return reverse('users:collection-league', kwargs={
            'username': self.username,
            'league_slug': league.slug,
        })

    def get_following_url(self):
        return reverse('users:following', kwargs={
            'username': self.username
        })

    def get_followers_url(self):
        return reverse('users:followers', kwargs={
            'username': self.username
        })

    def get_profile_url(self):
        return self.get_absolute_url()

    def get_packs_url(self):
        return reverse('users:packs', kwargs={
            'username': self.username
        })

    def get_password_change_url(self):
        return reverse('users:password_change', kwargs={
            'username': self.username
        })

    def get_settings_url(self):
        return reverse('users:settings', kwargs={
            'username': self.username
        })

    def get_squads_url(self):
        return reverse('users:squads', kwargs={
            'username': self.username
        })

    def get_username(self):
        return self.username

    def get_short_name(self):
        return self.get_username()

    def get_full_name(self):
        return self.get_username()

    def add_follower(self, follower):
        follower = UserFollowers.objects.get_or_create(
            from_user=self,
            to_user=follower)

        return follower[0]

    def remove_follower(self, follower):
        UserFollowers.objects.filter(
            from_user=self,
            to_user=follower).delete()

        return


sitemaps.register(User)


class UserFollowers(models.Model):
    from_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='to_user')

    def __str__(self):
        return f"{self.to_user}'s followers"


class FavouritePlayers(models.Model):
    user = AutoOneToOneField('users.User', on_delete=models.CASCADE)
    players = models.ManyToManyField('players.Player', blank=True)

    def __str__(self):
        return f"{self.user}'s favourite players"


class CollectionPlayer(models.Model):
    collection = models.ForeignKey('users.CardCollection', on_delete=models.CASCADE)
    player = models.ForeignKey('players.Player', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.collection.user}'s {self.player} ({self.player.rating})"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        club = self.player.club
        collected_players = [x
                             for x in self.collection.user.cardcollection.players(manager='cards').filter(club=club)]

        if club.total_players == len(collected_players):
            create_action(self.collection.user, 'completed collection for', club)


class CardCollection(models.Model):
    user = AutoOneToOneField('users.User', on_delete=models.CASCADE)
    players = models.ManyToManyField('players.Player', blank=True, through='users.CollectionPlayer')

    def __str__(self):
        return f"{self.user}'s card collection"
