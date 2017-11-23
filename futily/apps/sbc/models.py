import json

from cms.apps.pages.models import ContentBase, Page
from cms.models import SearchMetaBase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from futily.apps.packs.models import PackType
from futily.apps.players.models import Player
from futily.apps.squads.models import FORMATION_CHOICES


class SquadBuildingChallenges(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.sbc.urls'

    def __str__(self):
        return self.page.title


class SquadBuilderChallengeCategory(SearchMetaBase):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    ea_id = models.IntegerField(unique=True, blank=True, null=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'SBC Category'
        verbose_name_plural = 'SBC Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'{get_default_sbcs_page().get_absolute_url()}{self.slug}'


class SquadBuilderChallengeSet(SearchMetaBase):

    page = models.ForeignKey('sbc.SquadBuildingChallenges', blank=False, null=True)

    ea_id = models.IntegerField()
    trophy_id = models.IntegerField()

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    end_time = models.DateTimeField(blank=True, null=True)

    category = models.ForeignKey('sbc.SquadBuilderChallengeCategory')
    awards = models.ManyToManyField('sbc.SquadBuilderChallengeAward', blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'SBC Set'
        verbose_name_plural = 'SBC Sets'

    def __str__(self):
        return self.title

    def _get_permalink_for_page(self, name):
        return self.page.page.reverse(name, kwargs={
            'slug': self.slug,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page('set')

    def render_card(self, has_link=False):
        return render_to_string('sbc/includes/set.html', {
            'set': self,
            'has_link': has_link,
        })


class SquadBuilderChallenge(SearchMetaBase):

    set = models.ForeignKey('sbc.SquadBuilderChallengeSet')

    ea_id = models.IntegerField(unique=True)
    trophy_id = models.IntegerField()

    title = models.CharField(max_length=255)
    slug = models.SlugField()

    description = models.TextField()
    formation = models.CharField(max_length=10, choices=FORMATION_CHOICES)
    end_time = models.DateField(blank=True, null=True)

    awards = models.ManyToManyField('sbc.SquadBuilderChallengeAward')
    requirements = models.ManyToManyField('sbc.SquadBuilderChallengeRequirement')

    requirements_operation = models.CharField(max_length=255, choices=[(
        ('AND', 'AND'),
        ('OR', 'OR'),
    )])

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['title']
        verbose_name = 'SBC Challenge'
        verbose_name_plural = 'SBC Challenges'

    def __str__(self):
        return self.title

    def _get_permalink_for_page(self, name):
        return self.set.page.page.reverse(name, kwargs={
            'set_slug': self.set.slug,
            'slug': self.slug,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page('challenge')

    def get_builder_url(self):
        return self._get_permalink_for_page('challenge_builder')

    def render_card(self):
        return render_to_string('sbc/includes/challenge.html', {
            'challenge': self,
        })


class SquadBuilderChallengeRequirement(models.Model):
    """
    TEAM_STAR_RATING: Minimum star rating the team needs to be,
    TEAM_CHEMISTRY: Minimum chemistry the team needs to be,
    PLAYER_COUNT: X amount of players needed at a certain SCOPE,
    SAME_NATION_COUNT: Minimum amount of players from X nation,
    SAME_LEAGUE_COUNT: Minimum amount of players from X league,
    SAME_CLUB_COUNT: Minimum amount of players from X club,
    NATION_COUNT: X amount nations needed,
    LEAGUE_COUNT: X amount of leagues needed,
    CLUB_COUNT: X amount of clubs needed,
    TEAM_RATING: Minimum rating a team needs to be,
    """
    type = models.CharField(max_length=255)
    type_value = models.IntegerField(blank=True, null=True)

    scope = models.CharField(max_length=255, choices=[
        ('exact', 'exact'),
        ('gte', 'gte'),
        ('lte', 'lte'),
    ])

    club = models.ForeignKey('clubs.Club', blank=True, null=True)
    league = models.ForeignKey('leagues.League', blank=True, null=True)
    nation = models.ForeignKey('nations.Nation', blank=True, null=True)

    rare_count = models.IntegerField(default=0)

    player_quality = models.CharField(max_length=255, blank=True, null=True, choices=[
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('legend', 'Legend'),
    ])
    player_rarity = models.CharField(max_length=255, blank=True, null=True, choices=[
        ('rare', 'Rare'),
        ('inform', 'Inform'),
        ('legend', 'Legend'),
    ])

    class Meta:
        verbose_name = 'SBC Requirement'
        verbose_name_plural = 'SBC Requirements'

    def __str__(self):
        return f'{self.type} {self.scope} {self.type_value}'

    @property
    def to_string(self):
        SCOPE_SCHEMA = {
            'gte': 'Min.',
            'lte': 'Max',
            'exact': 'Exactly'
        }

        scope = SCOPE_SCHEMA[self.scope]

        if self.type == 'TEAM_CHEMISTRY':
            return f'{scope} Chemistry: {self.type_value}'
        elif self.type == 'TEAM_RATING_1_TO_100':
            return f'{scope} Rating: {self.type_value}'
        elif self.type == 'PLAYER_COUNT':
            if self.club:
                return f'{scope} {self.type_value} players from {self.club}'
            elif self.league:
                return f'{scope} {self.type_value} players from {self.league}'
            elif self.nation:
                return f'{scope} {self.type_value} players from {self.nation}'
            elif self.player_rarity:
                return f'{scope} {self.type_value} {self.player_rarity} players'

            return f'{scope} {self.type_value} players'
        elif self.type == 'SAME_NATION_COUNT':
            return f'{scope} {self.type_value} players from the same Nation'
        elif self.type == 'SAME_LEAGUE_COUNT':
            return f'{scope} {self.type_value} players from the same League'
        elif self.type == 'SAME_CLUB_COUNT':
            return f'{scope} {self.type_value} players from the same Club'
        elif self.type == 'NATION_COUNT':
            return f'{scope} {self.type_value} Nationalities needed'
        elif self.type == 'LEAGUE_COUNT':
            return f'{scope} {self.type_value} Leagues needed'
        elif self.type == 'CLUB_COUNT':
            return f'{scope} {self.type_value} Clubs needed'

    @property
    def to_json_string(self):
        SCOPE_SCHEMA = {
            'gte': 'Min.',
            'lte': 'Max',
            'exact': 'Exactly'
        }

        scope = SCOPE_SCHEMA[self.scope]
        values = {
            'scope': self.scope,
            'value': self.type_value,
        }

        if self.type == 'TEAM_CHEMISTRY':
            values['type'] = 'chemistry'
        elif self.type == 'TEAM_RATING_1_TO_100':
            values['type'] = 'rating'
        elif self.type == 'PLAYER_COUNT':
            if self.club:
                values['type'] = 'club'
                values['clubId'] = self.club.ea_id
            elif self.league:
                values['type'] = 'league'
                values['leagueId'] = self.league.ea_id
            elif self.nation:
                values['type'] = 'nation'
                values['nationId'] = self.nation.ea_id
            elif self.player_rarity:
                values['type'] = 'rares'
            else:
                values['type'] = 'player_count'
        elif self.type == 'SAME_CLUB_COUNT':
            values['type'] = 'same_club'
        elif self.type == 'SAME_LEAGUE_COUNT':
            values['type'] = 'same_league'
        elif self.type == 'SAME_NATION_COUNT':
            values['type'] = 'same_nation'
        elif self.type == 'NATION_COUNT':
            values['type'] = 'unique_nation'
        elif self.type == 'LEAGUE_COUNT':
            values['type'] = 'unique_league'
        elif self.type == 'CLUB_COUNT':
            values['type'] = 'unique_club'

        return json.dumps(values)

    @property
    def to_db_dict(self):
        scope = f'__{self.scope}' if self.scope != 'exact' else ''

        if self.type == 'TEAM_CHEMISTRY':
            return {f'chemistry{scope}': self.type_value}
        elif self.type == 'TEAM_RATING':
            return {f'rating{scope}': self.type_value}
        elif self.type == 'PLAYER_COUNT':
            if self.club:
                return {
                    'players__player__club': self.club,
                    f'players_total{scope}': self.type_value
                }
            elif self.league:
                return {
                    'players__player__league': self.league,
                    f'players_total{scope}': self.type_value
                }
            elif self.nation:
                return {
                    'players__player__nation': self.nation,
                    f'players_total{scope}': self.type_value
                }
        elif self.type == 'SAME_NATION_COUNT':
            return {'same_nation_count__gte': self.type_value}
        elif self.type == 'SAME_LEAGUE_COUNT':
            return {'same_league_count__gte': self.type_value}
        elif self.type == 'SAME_CLUB_COUNT':
            return {'same_club_count__gte': self.type_value}
        elif self.type == 'NATION_COUNT':
            return {'same_nation_count__lte': self.type_value}
        elif self.type == 'LEAGUE_COUNT':
            return {'same_league_count__lte': self.type_value}
        elif self.type == 'CLUB_COUNT':
            return {'same_club_count__lte': self.type_value}

    def render_builder(self):
        return render_to_string('sbc/includes/requirement_builder.html', {
            'requirement': self,
        })


class SquadBuilderChallengeAward(models.Model):
    type = models.CharField(max_length=255, choices=[
        ('coin', 'Coin'),
        ('item', 'Item'),
        ('pack', 'Pack'),
    ])

    # Not sure what these are
    count = models.IntegerField(blank=True, null=True)

    # 1 == bronze, 2 == silver, 3 == gold
    hal_id = models.IntegerField()

    # item_data basically is the player
    player = models.ForeignKey('players.Player', blank=True, null=True)
    pack = models.ForeignKey('packs.PackType', blank=True, null=True)

    # This gets set if the type is coins
    value = models.IntegerField(blank=True, null=True)

    is_coins = models.BooleanField(default=False)
    is_item = models.BooleanField(default=False)
    is_pack = models.BooleanField(default=False)
    is_untradeable = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SBC Award'
        verbose_name_plural = 'SBC Awards'

    def __str__(self):
        return f'{self.type} {self.value}'

    def get_item(self):
        try:
            return Player.objects.get(ea_id=self.value)
        except Player.DoesNotExist:
            return None

    def get_pack(self):
        try:
            return PackType.objects.get(ea_id=self.value)
        except PackType.DoesNotExist:
            return None

    def render(self, has_link=False):
        return render_to_string('sbc/includes/award.html', {
            'award': self,
            'has_link': has_link,
        })


def get_default_sbcs_page():
    """Returns the default nations page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(SquadBuildingChallenges),
        ).order_by('left').first()

    except IndexError:
        return None


def get_default_sbc_page():
    """Returns the default nation page for the site."""
    page = get_default_sbcs_page()

    if page:
        return page.content

    return None
