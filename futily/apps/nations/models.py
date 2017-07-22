from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


class Nations(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.nations.urls'

    def __str__(self):
        return self.page.title


class Nation(PageBase):
    page = models.ForeignKey('Nations', null=True, blank=False)

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
        verbose_name = 'Nation'
        verbose_name_plural = 'Nations'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(force_insert, force_update, using, update_fields)

    def _get_permalink_for_page(self, page):
        return page.reverse('nation', kwargs={
            'slug': self.slug,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page(self.page.page)

    def players(self):
        return self.player_set.all().select_related('club', 'league', 'nation')


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
