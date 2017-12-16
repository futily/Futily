from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property


class Leagues(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.leagues.urls'

    def __str__(self):
        return self.page.title


class LeagueManager(models.Manager):
    def get_queryset(self):
        qs = super(LeagueManager, self).get_queryset()

        qs = qs.select_related('page', 'nation')

        return qs


class League(PageBase):
    objects = LeagueManager()

    page = models.ForeignKey('Leagues', null=True, blank=False)
    nation = models.ForeignKey('nations.Nation', null=True, blank=True)
    cached_url = models.CharField(max_length=255, blank=True, null=True)

    ea_id = models.PositiveIntegerField()

    name = models.CharField(max_length=100)
    name_abbr = models.CharField(max_length=100)

    average_rating = models.FloatField(default=0)
    total_players = models.PositiveIntegerField(default=0)
    total_bronze = models.PositiveIntegerField(default=0)
    total_silver = models.PositiveIntegerField(default=0)
    total_gold = models.PositiveIntegerField(default=0)
    total_legends = models.PositiveIntegerField(default=0)
    total_totw = models.PositiveIntegerField(default=0)
    total_special = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-average_rating', '-total_players', 'name']
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'

    def __str__(self):
        return self.name

    def _get_permalink_for_page(self, cached=True):
        if self.cached_url and cached:
            return self.cached_url

        url = self.page.page.reverse('league', kwargs={
            'slug': self.slug,
        })

        if url != self.cached_url:
            self.cached_url = url
            self.save()

        return url

    @cached_property
    def _get_absolute_url(self):
        return self._get_permalink_for_page()

    def get_absolute_url(self):
        return self._get_absolute_url

    @cached_property
    def has_players(self):
        return self.player_set.exists()

    def players(self):
        return self.player_set(manager='cards').all().select_related('club', 'league', 'nation')

    def list_informs(self):
        return self.total_special + self.total_totw

    def collected_count(self, user):
        return user.cardcollection.players.filter(league__id=self.id).count()


def get_default_leagues_page():
    """Returns the default leagues page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(Leagues),
        ).order_by('left').first()

    except IndexError:
        return None


def get_default_league_page():
    """Returns the default league page for the site."""
    page = get_default_leagues_page()

    if page:
        return page.content

    return None
