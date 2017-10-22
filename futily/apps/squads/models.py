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

        totws = [(squad.short_title, squad.get_absolute_url())
                 for squad in self.squad_set.filter(is_special=True, short_title__icontains='totw')]

        return regular_items + totws


class SquadManager(PageBaseManager):
    def get_queryset(self):
        return super(SquadManager, self).get_queryset().prefetch_related(
            Prefetch('players', queryset=SquadPlayer.objects.select_related('player'))
        )


class Squad(SearchMetaBase):

    objects = SquadManager()

    title = models.CharField(max_length=255, blank=True, null=True)
    short_title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    page = models.ForeignKey('Squads', blank=False, null=True)
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

    is_special = models.BooleanField(default=False)

    web_app_import = models.BooleanField(default=False)
    web_app_url = models.CharField(max_length=100, blank=True, null=True)

    small_image_url = models.CharField(max_length=255, blank=True, null=True)
    large_image_url = models.CharField(max_length=255, blank=True, null=True)

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
        return sorted([x.player for x in self.players.all()], key=lambda x: x.rating, reverse=True)


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


class SquadPlayer(models.Model):
    player = models.ForeignKey('players.Player')
    squad = models.ForeignKey(Squad)
    index = models.PositiveIntegerField(blank=True, null=True)
    position = models.CharField(max_length=3)
    chemistry = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.player.__str__()
