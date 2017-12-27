from cms import sitemaps
from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property


class Nations(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.nations.urls'

    def __str__(self):
        return self.page.title


class NationManager(models.Manager):
    def get_queryset(self):
        qs = super(NationManager, self).get_queryset().select_related('page')

        return qs


class Nation(PageBase):
    objects = NationManager()

    page = models.ForeignKey('Nations', null=True, blank=False)
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

    pack_weight = models.PositiveIntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_players', '-average_rating', 'name']
        verbose_name = 'Nation'
        verbose_name_plural = 'Nations'

    def __str__(self):
        return self.name

    def _get_permalink_for_page(self, cached=True):
        if self.cached_url and cached:
            return self.cached_url

        url = self.page.page.reverse('nation', kwargs={
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
        return self.player_set.all().select_related('club', 'league', 'nation')

    def list_informs(self):
        return self.total_special + self.total_totw


sitemaps.register(Nation)


def get_default_nations_page():
    """Returns the default nations page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(Nations),
        ).order_by('left').first()

    except IndexError:
        return None


def get_default_nation_page():
    """Returns the default nation page for the site."""
    page = get_default_nations_page()

    if page:
        return page.content

    return None
