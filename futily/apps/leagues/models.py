from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


class Leagues(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.leagues.urls'

    def __str__(self):
        return self.page.title


class LeagueManager(models.Manager):
    def get_queryset(self):
        qs = super(LeagueManager, self).get_queryset()

        qs = qs.select_related('nation')

        return qs


class League(PageBase):
    objects = LeagueManager()

    page = models.ForeignKey('Leagues', null=True, blank=False)
    nation = models.ForeignKey('nations.Nation', null=True, blank=True)

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
        ordering = ['-total_players', '-average_rating', 'name']
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(force_insert, force_update, using, update_fields)

    def _get_permalink_for_page(self, page):
        return page.reverse('league', kwargs={
            'slug': self.slug,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page(self.page.page)

    def players(self):
        return self.player_set.all().select_related('club', 'league', 'nation')


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
