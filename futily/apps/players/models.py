import json
import operator
import random
import unicodedata
from functools import reduce

from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Q
from django.template.loader import render_to_string
from django.utils.datetime_safe import date
from django.utils.functional import cached_property
from django.utils.text import slugify

from futily.apps.prices.models import Price
from futily.apps.squads.models import Squad

from .constants import (BASE_COLOR_CHOICES, POSITION_CHOICES,
                        POSITION_LINE_CHOICES, QUALITY_CHOICES,
                        SPECIAL_COLOR_CHOICES, WORKRATE_CHOICES)


class Players(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.players.urls'

    def __str__(self):
        return self.page.title

    @property
    def navigation_items(self):
        return [
            ('Latest', self.page.reverse('latest_players')),
            ('Perfect chemistry', self.page.reverse('perfect_chemistry')),
        ]


class Source(models.Model):
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    ea_url = models.CharField(max_length=255, blank=True, null=True)

    order = models.PositiveIntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', 'order']

    def __str__(self):
        return self.title

    def clean(self):
        self.slug = slugify(self.short_title)

        super(Source, self).clean()


STAT_VALIDATOR = [MinValueValidator(0), MaxValueValidator(99)]


class PlayerManager(models.Manager):
    def get_queryset(self):
        qs = super(PlayerManager, self).get_queryset().select_related('page', 'page__page', 'club', 'league', 'nation')

        return qs


class PlayerCardManager(models.Manager):
    def get_queryset(self):
        qs = super(
            PlayerCardManager,
            self) .get_queryset() .select_related(
            'club',
            'league',
            'nation',
            'page',
            'page__page') .only(
            'id',
            'page',
            'cached_url',
            'club',
            'league',
            'nation',
            'color',
            'rating',
            'position',
            'ea_id',
            'name',
            'work_rate_att',
            'work_rate_def',
            'skill_moves',
            'weak_foot',
            'card_att_1',
            'card_att_2',
            'card_att_3',
            'card_att_4',
            'card_att_5',
            'card_att_6',
            'is_gk')
        # .defer('first_name', 'last_name', 'common_name', 'english_names', 'ea_id_base', 'image', 'image_sm',
        #        'image_md', 'image_lg', 'image_special_md_totw', 'image_special_lg_totw', 'position_full',
        #        'position_line', 'play_style', 'play_style_id', 'height', 'weight', 'birth_date', 'acceleration',
        #        'aggression', 'agility', 'balance', 'ball_control', 'crossing', 'curve', 'dribbling', 'finishing',
        #        'free_kick_accuracy', 'heading_accuracy', 'interceptions', 'jumping', 'long_passing', 'long_shots',
        #        'marking', 'penalties', 'positioning', 'potential', 'reactions', 'short_passing', 'shot_power',
        #        'sliding_tackle', 'sprint_speed', 'standing_tackle', 'stamina', 'strength', 'vision', 'volleys',
        #        'gk_diving', 'gk_handling', 'gk_kicking', 'gk_positioning', 'gk_reflexes', 'total_stats',
        #        'total_ingame_stats', 'foot', 'specialities', 'traits', 'player_type', 'item_type', 'model_name',
        #        'source', 'is_special_type', 'pack_weight', 'created', 'modified')

        return qs


class Player(PageBase):  # pylint: disable=too-many-public-methods, too-many-instance-attributes
    cards = PlayerCardManager()
    objects = PlayerManager()

    page = models.ForeignKey('Players', null=True, blank=False)
    cached_url = models.CharField(max_length=255, blank=True, null=True)

    club = models.ForeignKey('clubs.Club', null=True, blank=False, db_index=True)
    league = models.ForeignKey('leagues.League', null=True, blank=False, db_index=True)
    nation = models.ForeignKey('nations.Nation', null=True, blank=False, db_index=True)

    ea_id_base = models.PositiveIntegerField(db_index=True)
    ea_id = models.PositiveIntegerField(unique=True, db_index=True)

    name = models.CharField(max_length=100, db_index=True)
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

    rating_defensive = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    rating_anchor = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    rating_creative = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)
    rating_attacking = models.PositiveIntegerField(default=0, null=True, blank=False, validators=STAT_VALIDATOR)

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
    color = models.CharField(max_length=100, null=True, blank=False, choices=BASE_COLOR_CHOICES + SPECIAL_COLOR_CHOICES)
    source = models.ForeignKey('players.Source', null=True, blank=True)

    is_gk = models.BooleanField(default=False)
    is_special_type = models.BooleanField(default=False)

    likes = models.IntegerField(default=0)
    has_perfect_chem_links = models.PositiveIntegerField(default=False)

    pack_value = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', 'name']
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)

        self.english_names = [
            # pylint: disable=bad-continuation
            unicodedata
            .normalize('NFKD', getattr(self, x))
            .encode('ascii', 'ignore')
            .decode('utf-8')
            for x in ['name', 'first_name', 'last_name', 'common_name']
        ]
        first_name = unicodedata \
            .normalize('NFKD', self.first_name) \
            .encode('ascii', 'ignore') \
            .decode('utf-8')
        last_name = unicodedata \
            .normalize('NFKD', self.last_name) \
            .encode('ascii', 'ignore') \
            .decode('utf-8')
        self.english_names.append(f'{first_name} {last_name}')

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

        rating_schemas = {
            'defensive': {
                'ball_control': 0.09,
                'reactions': 0.09,
                'heading_accuracy': 0.1,
                'interceptions': 0.09,
                'marking': 0.09,
                'sliding_tackle': 0.1,
                'standing_tackle': 0.09,
                'aggression': 0.09,
                'jumping': 0.1,
                'stamina': 0.09,
                'strength': 0.08,
            },
            'anchor': {
                'acceleration': 0.09,
                'short_passing': 0.1,
                'agility': 0.09,
                'balance': 0.1,
                'reactions': 0.1,
                'interceptions': 0.1,
                'sliding_tackle': 0.1,
                'standing_tackle': 0.1,
                'aggression': 0.1,
                'stamina': 0.11,
            },
            'creative': {
                'long_shots': 0.1,
                'positioning': 0.1,
                'shot_power': 0.1,
                'crossing': 0.1,
                'short_passing': 0.1,
                'vision': 0.1,
                'ball_control': 0.1,
                'dribbling': 0.1,
                'reactions': 0.1,
                'stamina': 0.1,
            },
            'attacking': {
                'acceleration': 0.08,
                'finishing': 0.09,
                'long_shots': 0.08,
                'positioning': 0.09,
                'shot_power': 0.08,
                'volleys': 0.08,
                'curve': 0.08,
                'agility': 0.08,
                'ball_control': 0.09,
                'dribbling': 0.08,
                'reactions': 0.09,
                'stamina': 0.08,
            },
        }

        def reduceSchemas(acc, item):
            acc += getattr(self, item[0]) * item[1]

            return acc

        self.rating_defensive = reduce(reduceSchemas, rating_schemas['defensive'].items(), 0)
        self.rating_anchor = reduce(reduceSchemas, rating_schemas['anchor'].items(), 0)
        self.rating_creative = reduce(reduceSchemas, rating_schemas['creative'].items(), 0)
        self.rating_attacking = reduce(reduceSchemas, rating_schemas['attacking'].items(), 0)

        self.has_perfect_chem_links = bool(self.get_chemistry_players(amount=1)['perfect'])

        super().save(force_insert, force_update, using, update_fields)

    def _get_permalink_for_page(self, name='player', extra_kwargs=None, cached=True):
        if self.cached_url and cached:
            return self.cached_url

        url_kwargs = {
            'pk': self.pk,
            'slug': self.slug,
        }

        if extra_kwargs and isinstance(extra_kwargs, dict):
            url_kwargs = {**url_kwargs, **extra_kwargs}

        url = self.page.page.reverse(name, kwargs=url_kwargs)

        if url != self.cached_url and name == 'player':
            self.cached_url = url
            self.save()

        return url

    @cached_property
    def _get_absolute_url(self):
        return self._get_permalink_for_page()

    def get_absolute_url(self):
        return self._get_absolute_url

    def get_chemistry_absolute_url(self):
        return self._get_permalink_for_page(name='player_chemistry', cached=False)

    def get_chemistry_type_absolute_url(self, chem_type):
        if not chem_type:
            raise Exception('Please supply a chem_type')

        return self._get_permalink_for_page(name='player_chemistry_type',
                                            extra_kwargs={'chem_type': chem_type},
                                            cached=False)

    def get_similar_absolute_url(self):
        return self._get_permalink_for_page(name='player_similar', cached=False)

    def get_compare_absolute_url(self):
        return self._get_permalink_for_page(name='player_compare', cached=False)

    def get_favourite_absolute_url(self):
        return self._get_permalink_for_page(name='player_favourite', cached=False)

    def get_source_squad(self):
        return Squad.objects.get(title=self.source.title, is_special=True)

    def render_card(self, size='medium', faded=False, rpp=False, color=None, chemistry=None, has_link=True, new=False):
        if size not in ['small', 'medium', 'large']:
            raise TypeError('size argument should be 1 of "small", "normal" or "large"')

        return render_to_string('players/includes/card.html', {
            'player': self,
            'size': size,
            'faded': faded,
            'rpp': rpp,
            'color': color,
            'chemistry': chemistry,
            'el': 'a' if has_link else 'div',
            'new': new,
        })

    @cached_property
    def age(self):
        born = self.birth_date
        today = date.today()

        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @cached_property
    def card_json_data(self):
        return json.dumps({
            'rating': self.rating,
            'color': self.color,
            'position': self.position,
            'ea_id': self.ea_id,
            'card_att_1': self.card_att_1,
            'card_att_2': self.card_att_2,
            'card_att_3': self.card_att_3,
            'card_att_4': self.card_att_4,
            'card_att_5': self.card_att_5,
            'card_att_6': self.card_att_6,
            'club': {
                'name': self.club.name,
                'ea_id': self.club.ea_id,
            }
        })

    @cached_property
    def card_stats(self):
        return [
            ('PAC' if not self.is_gk else 'DIV', self.card_att_1),
            ('SHO' if not self.is_gk else 'HAN', self.card_att_2),
            ('PAS' if not self.is_gk else 'KIC', self.card_att_3),
            ('DRI' if not self.is_gk else 'REF', self.card_att_4),
            ('DEF' if not self.is_gk else 'SPD', self.card_att_5),
            ('PHY' if not self.is_gk else 'POS', self.card_att_6)
        ]

    @cached_property
    def card_stats_full(self):
        return [
            ('Pace' if not self.is_gk else 'Diving', self.card_att_1),
            ('Shooting' if not self.is_gk else 'Handling', self.card_att_2),
            ('Passing' if not self.is_gk else 'Kicking', self.card_att_3),
            ('Dribbling' if not self.is_gk else 'Reflexes', self.card_att_4),
            ('Defending' if not self.is_gk else 'Speed', self.card_att_5),
            ('Physical' if not self.is_gk else 'Positioning', self.card_att_6)
        ]

    @cached_property
    def similar_coefficient(self):
        return self.total_ingame_stats / 100 / 2.5

    @cached_property
    def average_ps_price(self):
        try:
            return int(Price.objects.filter(market='ps', player__pk=self.pk)[:10].aggregate(Avg('value'))['value__avg'])
        except Exception as e:
            return 0

    @cached_property
    def average_xbox_price(self):
        try:
            return int(Price.objects.filter(market='xb', player__pk=self.pk)[:10].aggregate(Avg('value'))['value__avg'])
        except Exception as e:
            return 0

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

    def ingame_stat_groups(self):
        return [
            {'label': 'pace', 'field': 'card_att_1', 'items': ['acceleration', 'sprint_speed']},
            {
                'label': 'shooting', 'field': 'card_att_2', 'items': ['finishing', 'long_shots', 'penalties',
                                                                      'positioning', 'shot_power', 'volleys']
            },
            {
                'label': 'passing', 'field': 'card_att_3', 'items': ['crossing', 'curve', 'free_kick_accuracy',
                                                                     'long_passing', 'short_passing', 'vision']
            },
            {
                'label': 'dribbling', 'field': 'card_att_4', 'items': ['agility', 'balance', 'ball_control',
                                                                       'dribbling', 'reactions']
            },
            {
                'label': 'defending', 'field': 'card_att_5', 'items': ['heading_accuracy', 'interceptions', 'marking',
                                                                       'sliding_tackle', 'standing_tackle']
            },
            {'label': 'physicality', 'field': 'card_att_6', 'items': ['aggression', 'jumping', 'stamina', 'strength']},
        ]

    @staticmethod
    def get_similar_positions(position):
        schema = {
            'GK': ['GK'],
            'RWB': ['RWB', 'RB'],
            'RB': ['RWB', 'RB'],
            'CB': ['CB'],
            'LB': ['LWB', 'LB'],
            'LWB': ['LWB', 'LB'],
            'CDM': ['CDM', 'CM', 'CAM'],
            'CM': ['CDM', 'CM', 'CAM'],
            'CAM': ['CDM', 'CM', 'CAM'],
            'RM': ['RM', 'RW', 'RF'],
            'RW': ['RM', 'RW', 'RF'],
            'RF': ['RM', 'RW', 'RF'],
            'LM': ['LM', 'LW', 'LF'],
            'LW': ['LM', 'LW', 'LF'],
            'LF': ['LM', 'LW', 'LF'],
            'CF': ['CAM', 'CF', 'ST'],
            'ST': ['CF', 'ST'],
        }

        return schema[position]

    def get_variants(self):
        if self.color == 'legend':
            return Player.objects.filter(color='legend', slug=self.slug)

        # Get all the different versions of the base card
        return Player.objects.filter(ea_id_base=self.ea_id_base).exclude(id=self.id)

    def get_chemistry_players(self, amount=None):
        # We only need to get certain positions as not all positions can link with other positions
        position_schema = {
            'GK': ['CB'],
            'RB': ['CB', 'RM', 'RW', 'RF', 'CDM', 'CM', 'CAM', 'CF', 'ST'],
            'RWB': ['CB', 'RM', 'RW', 'RF', 'CDM', 'CM', 'CAM', 'CF', 'ST'],
            'CB': ['GK', 'CB', 'RB', 'RWB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF', 'LM',
                   'LW', 'LF'],
            'LB': ['CB', 'RM', 'RW', 'RF', 'CDM', 'CM', 'CAM', 'CF', 'ST'],
            'LWB': ['CB', 'RM', 'RW', 'RF', 'CDM', 'CM', 'CAM', 'CF', 'ST'],
            'CDM': ['RB', 'RWB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF', 'LM', 'LW', 'LF'],
            'CM': ['RB', 'RWB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF', 'LM', 'LW', 'LF'],
            'CAM': ['RB', 'RWB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF', 'LM', 'LW', 'LF'],
            'CF': ['RB', 'RWB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF', 'LM', 'LW', 'LF'],
            'ST': ['RB', 'RWB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF', 'LM', 'LW', 'LF'],
            'RM': ['CB', 'RB', 'RWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF'],
            'RW': ['CB', 'RB', 'RWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF'],
            'RF': ['CB', 'RB', 'RWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'RM', 'RW', 'RF'],
            'LM': ['CB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'LM', 'LW', 'LF'],
            'LW': ['CB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'LM', 'LW', 'LF'],
            'LF': ['CB', 'LB', 'LWB', 'CDM', 'CM', 'CAM', 'CF', 'ST', 'LM', 'LW', 'LF'],
        }

        initial_qs = Player.objects.filter(position__in=position_schema[self.position])

        perfect_chem = initial_qs.filter(club=self.club, nation=self.nation).exclude(ea_id_base=self.ea_id_base)
        strong_chem = initial_qs.filter(
            Q(Q(league=self.league), Q(nation=self.nation), ~Q(club=self.club)) |
            Q(club=self.club)
        ).exclude(ea_id_base=self.ea_id_base)
        weak_chem = initial_qs.filter(
            Q(Q(league=self.league), ~Q(nation=self.nation), ~Q(club=self.club)) |
            Q(Q(nation=self.nation), ~Q(league=self.league))
        ).exclude(ea_id_base=self.ea_id_base)

        if amount:
            perfect_chem = perfect_chem[:amount]
            strong_chem = strong_chem[:amount]
            weak_chem = weak_chem[:amount]

        return {
            'perfect': perfect_chem,
            'strong': strong_chem,
            'weak': weak_chem,
        }

    def get_serializer_data(self):
        from .serializers import PlayerSerializer

        return json.dumps(PlayerSerializer(self).data)

    def get_initial_chemistry_players(self, chem_type='perfect'):
        players = self.get_chemistry_players(18)

        if len(players[chem_type]) > 6:
            return random.sample(list(players[chem_type]), 6)

        return players[chem_type]

    def get_similar_players(self, amount=None, sort=None):
        sort = sort if sort else 'ea_id'
        coefficient = self.similar_coefficient
        schema = {
            'GK': [1, 2, 3, 4, 5, 6],
            'RWB': [1, 5, 6],
            'RB': [1, 5, 6],
            'CB': [1, 5, 6],
            'LB': [1, 5, 6],
            'LWB': [1, 5, 6],
            'CDM': [1, 2, 3, 5, 6],
            'CM': [1, 2, 3, 4, 5, 6],
            'CAM': [1, 2, 3, 4, 6],
            'RM': [1, 2, 3, 4, 6],
            'RW': [1, 2, 3, 4, 6],
            'RF': [1, 2, 3, 4, 6],
            'LM': [1, 2, 3, 4, 6],
            'LW': [1, 2, 3, 4, 6],
            'LF': [1, 2, 3, 4, 6],
            'CF': [1, 2, 3, 4, 6],
            'ST': [1, 2, 3, 4, 6],
        }

        q_objs = [
            Q(
                (
                    f'card_att_{val}__range',
                    [getattr(self, f'card_att_{val}') - coefficient, getattr(self, f'card_att_{val}') + coefficient]
                )
            ) for val in schema[self.position]
        ]

        players = Player.cards \
            .filter(reduce(operator.and_, q_objs), position__in=self.get_similar_positions(self.position)) \
            .exclude(ea_id=self.ea_id) \
            .order_by(sort)

        if not sort:
            players = players.distinct(sort)

        if amount:
            players = players[:amount]

        return players

    def get_initial_similar_players(self):
        players = self.get_similar_players(18)

        if len(players) > 6:
            return random.sample(list(players), 6)

        return players


class Icon(models.Model):
    player = models.ForeignKey('players.Player')

    club_team_stats = JSONField(blank=True, null=True)
    national_team_stats = JSONField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.player


class PlayerRating(models.Model):
    player = models.OneToOneField('players.Player', db_index=True, on_delete=models.CASCADE)

    score = models.IntegerField(default=0, db_index=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.player}'s rating"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.player.likes = self.score
        self.player.save()

        super().save(force_insert, force_update, using, update_fields)

    def to_dict(self):
        return {
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'score': self.score
        }


class VoteManager(models.Manager):
    def vote(self, player, user, action):
        rating, created = PlayerRating.objects.get_or_create(player=player)  # pylint: disable=unused-variable
        existing_vote = self.filter(rating__player=player, user=user).first()

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

    def up(self, player, user):
        self.vote(player, user, 'up')

    def down(self, player, user):
        self.vote(player, user, 'down')


class Vote(models.Model):
    votes = VoteManager()

    user = models.ForeignKey('users.User', db_index=True)
    rating = models.OneToOneField('players.PlayerRating', db_index=True)
    action = models.CharField(max_length=5, choices=[('up', 'Up'), ('down', 'Down')])

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'rating']

    def __str__(self):
        return f"{self.user}'s rating for {self.rating.player}"


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
