from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, Page
from cms.models import PageBase
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

from ..fields import ChoiceArrayField


class Packs(ContentBase):
    classifier = 'objects'
    urlconf = 'futily.apps.packs.urls'

    def __str__(self):
        return self.page.title


color_choices = [
    ('award_winner', 'Award winner'),
    ('bronze', 'Bronze'),
    ('confederation_champions_motm', 'Confederation champions MOTM'),
    ('fut_birthday', 'FUT Birthday'),
    ('futties_winner', 'Futties winner'),
    ('gold', 'Gold'),
    ('gotm', 'GOTM'),
    ('halloween', 'Halloween'),
    ('imotm', 'iMOTM'),
    ('legend', 'Legend'),
    ('motm', 'MOTM'),
    ('movember', 'Movember'),
    ('ones_to_watch', 'Ones to watch'),
    ('pink', 'Pink'),
    ('purple', 'Purple'),
    ('rare_bronze', 'Rare Bronze'),
    ('rare_gold', 'Rare Gold'),
    ('rare_silver', 'Rare Silver'),
    ('record_breaker', 'Record breaker'),
    ('sbc_base', 'SBC base'),
    ('silver', 'Silver'),
    ('st_patricks', 'St. Patricks'),
    ('tots_bronze', 'TOTS Bronze'),
    ('tots_gold', 'TOTS Gold'),
    ('tots_silver', 'TOTS Silver'),
    ('totw_bronze', 'TOTW Bronze'),
    ('totw_gold', 'TOTW Gold'),
    ('totw_silver', 'TOTW Silver'),
    ('toty', 'TOTY'),
]


class PackType(PageBase):
    page = models.ForeignKey('packs.Packs')

    description = models.TextField()
    image = ImageRefField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    ea_pack = models.BooleanField(default=True)
    ea_id = models.CharField(max_length=255, blank=True, null=True)

    quality = models.CharField(max_length=255, choices=[
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('special', 'Special'),
    ], default='special')

    roll_1_types = ChoiceArrayField(
        base_field=models.CharField(max_length=100, choices=color_choices),
        default=list, help_text='These are part of the "normal" rolls.',
    )
    roll_1_types_rating_min = models.PositiveIntegerField(default=75)
    roll_1_types_rating_max = models.PositiveIntegerField(default=99)

    roll_2_types = ChoiceArrayField(
        base_field=models.CharField(max_length=100, choices=color_choices),
        default=list, help_text='These are part of the "normal" rolls.',
    )
    roll_2_types_rating_min = models.PositiveIntegerField(default=75)
    roll_2_types_rating_max = models.PositiveIntegerField(default=99)

    roll_3_types = ChoiceArrayField(
        base_field=models.CharField(max_length=100, choices=color_choices),
        default=list, help_text='These are part of the "normal" rolls.',
    )
    roll_3_types_rating_min = models.PositiveIntegerField(default=75)
    roll_3_types_rating_max = models.PositiveIntegerField(default=99)

    roll_4_types = ChoiceArrayField(
        base_field=models.CharField(max_length=100, choices=color_choices),
        default=list, help_text='These are part of the "rare" rolls.',
    )
    roll_4_types_rating_min = models.PositiveIntegerField(default=75)
    roll_4_types_rating_max = models.PositiveIntegerField(default=99)

    roll_5_types = ChoiceArrayField(
        base_field=models.CharField(max_length=100, choices=color_choices),
        default=list, help_text='These are part of the "rare" rolls.',
    )
    roll_5_types_rating_min = models.PositiveIntegerField(default=75)
    roll_5_types_rating_max = models.PositiveIntegerField(default=99)

    roll_6_types = ChoiceArrayField(
        base_field=models.CharField(max_length=100, choices=color_choices),
        default=list, help_text='These are part of the "rare" rolls.',
    )
    roll_6_types_rating_min = models.PositiveIntegerField(default=75)
    roll_6_types_rating_max = models.PositiveIntegerField(default=99)

    normal_count = models.PositiveIntegerField(default=0)
    rare_count = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-is_online', 'ea_id']

    def __str__(self):
        return self.title

    def _get_permalink_for_page(self, page):
        return page.reverse('type', kwargs={
            'slug': self.slug,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page(self.page.page)


class Pack(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)

    page = models.ForeignKey('packs.Packs', blank=False, null=True)
    user = models.ForeignKey('users.User')
    players = models.ManyToManyField('players.Player')
    type = models.ForeignKey('packs.PackType')

    value = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)

        super().save(force_insert, force_update, using, update_fields)

    def _get_permalink_for_page(self, page):
        return page.reverse('pack', kwargs={
            'pk': self.pk,
            'slug': self.slug,
        })

    def get_absolute_url(self):
        return self._get_permalink_for_page(self.page.page)


def get_default_packs_page():
    """Returns the default nations page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(Packs),
        ).order_by('left').first()

    except IndexError:
        return None


def get_default_pack_page():
    """Returns the default nation page for the site."""
    page = get_default_packs_page()

    if page:
        return page.content

    return None
