from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBaseManager, SearchMetaBase
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Prefetch
from django.utils.text import slugify

FORMATION_CHOICES = [
    ('3412', '3-4-1-2'),
    ('3421', '3-4-2-1'),
    ('343', '3-4-3'),
    ('352', '3-5-2'),
    ('41212', '4-1-2-1-2'),
    ('41212-2', '4-1-2-1-2 (2)'),
    ('4141', '4-1-4-1'),
    ('4231', '4-2-3-1'),
    ('4231-2', '4-2-3-1 (2)'),
    ('4222', '4-2-2-2'),
    ('4312', '4-3-1-2'),
    ('4321', '4-3-2-1'),
    ('433', '4-3-3'),
    ('433-2', '4-3-3 (2)'),
    ('433-3', '4-3-3 (3)'),
    ('433-4', '4-3-3 (4)'),
    ('433-5', '4-3-3 (5)'),
    ('4411', '4-4-1-1'),
    ('442', '4-4-2'),
    ('442-2', '4-4-2 (2)'),
    ('451', '4-5-1'),
    ('451-2', '4-5-1 (2)'),
    ('5212', '5-2-1-2'),
    ('5221', '5-2-2-1'),
    ('532', '5-3-2'),
]


class Squads(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.squads.urls'

    def __str__(self):
        return self.page.title

    @property
    def navigation_items(self):
        regular_items = [
            ('Builder', self.page.reverse('builder')),
            ("All TOTW's", self.page.reverse('totws')),
        ]

        totws = [
            (squad.short_title, squad.get_absolute_url())
            for squad in self.squad_set.filter(
                is_special=True,
                short_title__icontains='totw'
            ).only('is_special', 'short_title', 'page', 'pk')
        ]

        return regular_items + totws


class Squad(SearchMetaBase):

    title = models.CharField(max_length=255, blank=True, null=True)
    short_title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    page = models.ForeignKey('Squads', blank=False, null=True)
    sbc = models.ForeignKey('sbc.SquadBuilderChallenge', blank=False, null=True)
    user = models.ForeignKey('users.User', blank=True, null=True)

    players = models.ManyToManyField('players.Player', through='SquadPlayer', blank=True)
    formation = models.CharField(max_length=10, choices=FORMATION_CHOICES, default='442')
    chemistry = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    rating = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    attack = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    midfield = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    defence = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    pace = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    shooting = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    passing = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    dribbling = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    defending = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    physical = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0), MaxValueValidator(100)])

    loyalty = models.PositiveIntegerField(default=0)
    position_changes = models.PositiveIntegerField(default=0)

    is_special = models.BooleanField(default=False)

    web_app_import = models.BooleanField(default=False)
    web_app_url = models.CharField(max_length=100, blank=True, null=True)

    small_image_url = models.CharField(max_length=255, blank=True, null=True)
    large_image_url = models.CharField(max_length=255, blank=True, null=True)

    likes = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title or f'Squad {self.id}'

    def clean(self):
        if self.is_special:
            self.slug = slugify(self.short_title)

        super(Squad, self).clean()

    def _get_permalink_for_page(self, name):
        return self.page.page.reverse(name, kwargs={
            'pk': self.pk,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page('squad')

    def get_update_url(self):
        return self._get_permalink_for_page('squad-update')

    def get_copy_url(self):
        return self._get_permalink_for_page('squad-copy')

    def get_players(self):
        indexes = [index for index in range(0, 11)]

        for player in self.players.all():
            is_team = player.index <= 10

            if is_team:
                indexes[player.index] = player

        return [None if isinstance(x, int) else x for x in indexes]

    def get_player_objects(self):
        return sorted([x for x in self.players.all()], key=lambda x: x.rating, reverse=True)


class SquadPlayer(models.Model):
    player = models.ForeignKey('players.Player')
    squad = models.ForeignKey(Squad)
    index = models.PositiveIntegerField(blank=True, null=True)
    position = models.CharField(max_length=3)
    chemistry = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.player.__str__()


class SquadRating(models.Model):
    squad = models.OneToOneField('squads.Squad', db_index=True, on_delete=models.CASCADE)

    score = models.IntegerField(default=0, db_index=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.squad}'s rating"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.squad.likes = self.score
        self.squad.save()

        super().save(force_insert, force_update, using, update_fields)

    def to_dict(self):
        return {
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'score': self.score
        }


class VoteManager(models.Manager):
    def vote(self, squad, user, action):
        rating, created = SquadRating.objects.get_or_create(squad=squad)  # pylint: disable=unused-variable
        existing_vote = self.filter(rating__squad=squad, user=user).first()

        if existing_vote:
            old_action = existing_vote.action

            if old_action == 'up':
                rating.upvotes -= 1
            else:
                rating.downvotes -= 1

            existing_vote.action = action
            existing_vote.save()

        if action == 'up':
            rating.upvotes += 1
        else:
            rating.downvotes += 1

        rating.score = rating.upvotes - rating.downvotes
        rating.save()

        vote, created = self.get_or_create(rating=rating, user=user, action=action)  # pylint: disable=unused-variable

        return vote

    def up(self, squad, user):
        self.vote(squad, user, 'up')

    def down(self, squad, user):
        self.vote(squad, user, 'down')


class Vote(models.Model):
    votes = VoteManager()

    user = models.ForeignKey('users.User', db_index=True, related_name='squad_vote')
    rating = models.OneToOneField('squads.SquadRating', db_index=True)
    action = models.CharField(max_length=5, choices=[('up', 'Up'), ('down', 'Down')])

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'rating']

    def __str__(self):
        return f"{self.user}'s rating for {self.rating.squad}"


def get_default_squads_page():
    """Returns the default nations page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(Squads),
        ).order_by('left').first()

    except IndexError:
        return None


def get_default_squad_page():
    """Returns the default nation page for the site."""
    page = get_default_squads_page()

    if page:
        return page.content

    return None
