from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.datetime_safe import date
from django.utils.text import slugify

from .constants import (COLOR_CHOICES, POSITION_CHOICES, POSITION_LINE_CHOICES,
                        QUALITY_CHOICES, WORKRATE_CHOICES)


class Players(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.players.urls'

    def __str__(self):
        return self.page.title


class PlayerManager(models.Manager):
    def get_queryset(self):
        qs = super(PlayerManager, self).get_queryset().select_related('club', 'league', 'nation')

        return qs


class Source(models.Model):
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def clean(self):
        self.slug = slugify(self.short_title)

        super(Source, self).clean()


STAT_VALIDATOR = [MinValueValidator(0), MaxValueValidator(99)]


class Player(PageBase):
    objects = PlayerManager()

    page = models.ForeignKey('Players', null=True, blank=False)

    club = models.ForeignKey('clubs.Club', null=True, blank=False, db_index=True)
    league = models.ForeignKey('leagues.League', null=True, blank=False, db_index=True)
    nation = models.ForeignKey('nations.Nation', null=True, blank=False, db_index=True)

    ea_id_base = models.PositiveIntegerField(unique=True, db_index=True)
    ea_id = models.PositiveIntegerField(db_index=True)

    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    common_name = models.CharField(max_length=200, db_index=True)
    english_names = JSONField(null=True, blank=False, db_index=True)

    image = models.CharField(max_length=255, blank=True, null=True)
    image_sm = models.CharField(max_length=255, blank=True, null=True)
    image_md = models.CharField(max_length=255, blank=True, null=True)
    image_lg = models.CharField(max_length=255, blank=True, null=True)
    image_special_md_totw = models.CharField(max_length=255, blank=True, null=True)
    image_special_lg_totw = models.CharField(max_length=255, blank=True, null=True)

    position = models.CharField(max_length=10, choices=POSITION_CHOICES, null=True, blank=False)
    position_full = models.CharField(max_length=100, null=True, blank=False)
    position_line = models.CharField(max_length=10, choices=POSITION_LINE_CHOICES, null=True, blank=False)

    play_style = models.CharField(max_length=100, null=True, blank=False)
    play_style_id = models.CharField(max_length=100, null=True, blank=False)

    height = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    birth_date = models.DateField(null=True, blank=False)

    acceleration = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    aggression = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    agility = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    balance = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    ball_control = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    crossing = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    curve = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    dribbling = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    finishing = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    free_kick_accuracy = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    heading_accuracy = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    interceptions = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    jumping = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    long_passing = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    long_shots = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    marking = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    penalties = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    positioning = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    potential = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    reactions = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    short_passing = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    shot_power = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    sliding_tackle = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    sprint_speed = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    standing_tackle = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    stamina = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    strength = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    vision = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    volleys = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)

    gk_diving = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    gk_handling = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    gk_kicking = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    gk_positioning = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    gk_reflexes = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)

    total_stats = models.PositiveIntegerField(default=0, null=True, blank=False)
    total_ingame_stats = models.PositiveIntegerField(default=0, null=True, blank=False)

    foot = models.CharField(max_length=10, null=True, blank=False, choices=[
        ('Left', 'Left'),
        ('Right', 'Right'),
    ])
    skill_moves = models.PositiveIntegerField(default=0, null=True, blank=False)
    weak_foot = models.PositiveIntegerField(default=0, null=True, blank=False)

    card_att_1 = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    card_att_2 = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    card_att_3 = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    card_att_4 = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    card_att_5 = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    card_att_6 = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    rating = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR, db_index=True)

    specialities = JSONField(null=True, blank=True)
    traits = JSONField(null=True, blank=True)

    work_rate_att = models.CharField(max_length=10, null=True, blank=False, choices=WORKRATE_CHOICES)
    work_rate_def = models.CharField(max_length=10, null=True, blank=False, choices=WORKRATE_CHOICES)

    player_type = models.CharField(max_length=100, null=True, blank=False)
    item_type = models.CharField(max_length=100, null=True, blank=False)
    model_name = models.CharField(max_length=100, null=True, blank=False)
    quality = models.CharField(max_length=100, null=True, blank=False, choices=QUALITY_CHOICES)
    color = models.CharField(max_length=100, null=True, blank=False, choices=COLOR_CHOICES)
    source = models.ForeignKey('players.Source', null=True, blank=True)

    is_gk = models.BooleanField(default=False)
    is_special_type = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', 'common_name']
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.common_name)

        self.total_stats = (self.card_att_1 + self.card_att_2 + self.card_att_3 + self.card_att_4 +
                            self.card_att_5 + self.card_att_6)
        self.total_ingame_stats = (
            self.acceleration + self.aggression + self.agility + self.balance +
            self.ball_control + self.crossing + self.curve + self.dribbling +
            self.finishing + self.free_kick_accuracy + self.heading_accuracy +
            self.interceptions + self.jumping + self.long_passing + self.long_shots +
            self.marking + self.penalties + self.positioning + self.reactions +
            self.short_passing + self.shot_power + self.sliding_tackle + self.sprint_speed +
            self.standing_tackle + self.stamina + self.strength + self.vision + self.volleys
        )

        super().save(force_insert, force_update, using, update_fields)

    def _get_permalink_for_page(self, page):
        return page.reverse('player', kwargs={
            'slug': self.slug,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page(self.page.page)

    def render_card(self, size='sm'):
        return render_to_string('players/includes/card.html', {
            'player': self,
            'size': 'small' if size == 'sm' else 'large'
        })

    @property
    def age(self):
        born = self.birth_date
        today = date.today()

        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def card_stats(self):
        return [
            ('PAC' if not self.is_gk else 'DIV', self.card_att_1),
            ('DRI' if not self.is_gk else 'REF', self.card_att_4),
            ('SHO' if not self.is_gk else 'HAN', self.card_att_2),
            ('DEF' if not self.is_gk else 'SPD', self.card_att_5),
            ('PAS' if not self.is_gk else 'KIC', self.card_att_3),
            ('PHY' if not self.is_gk else 'POS', self.card_att_6)
        ]

    def ingame_stat_group_average(self, group):
        schema = {
            'pace': self.card_att_1,
            'dribbling': self.card_att_4,
            'shooting': self.card_att_2,
            'defending': self.card_att_5,
            'passing': self.card_att_3,
            'physicality': self.card_att_6,
        }

        return schema[group]


def get_default_players_page():
    """Returns the default players page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(Players),
        ).order_by('left')[0]
    except IndexError:
        return None


def get_default_player_page():
    """Returns the default player page for the site."""
    page = get_default_players_page()

    if page:
        return page.content

    return None
