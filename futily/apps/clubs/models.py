from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property


class Clubs(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.clubs.urls'

    def __str__(self):
        return self.page.title


class ClubManager(models.Manager):
    def get_queryset(self):
        qs = super(ClubManager, self).get_queryset()

        qs = qs.select_related('page', 'league')

        return qs


class Club(PageBase):
    objects = ClubManager()

    page = models.ForeignKey('Clubs', null=True, blank=False)
    league = models.ForeignKey('leagues.League', null=True, blank=True)
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
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'

    def __str__(self):
        return self.name

    def _get_permalink_for_page(self, cached=True):
        if self.cached_url and cached:
            return self.cached_url

        url = self.page.page.reverse('club', kwargs={
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

    def attackers(self):
        return self.players().filter(position_line='ATT')

    def midfielders(self):
        return self.players().filter(position_line='MID')

    def defenders(self):
        return self.players().filter(position_line='DEF')

    def goalkeepers(self):
        return self.players().filter(position_line='GK')

    def list_informs(self):
        return self.total_special + self.total_totw

    def collected_count(self, user):
        return user.cardcollection.players.filter(club__id=self.id).count()


def get_default_clubs_page():
    """Returns the default clubs page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(Clubs),
        ).order_by('left').first()

    except IndexError:
        return None


def get_default_club_page():
    """Returns the default club page for the site."""
    page = get_default_clubs_page()

    if page:
        return page.content

    return None
