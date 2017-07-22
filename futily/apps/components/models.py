from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import Page
from django.db import models


class CallToAction(models.Model):

    super_title = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=140)

    link_page = models.ForeignKey(Page, blank=True, null=True,
                                  help_text='If you want to link to an internal page, please use this.')
    link_url = models.CharField(max_length=200, blank=True, null=True,
                                help_text='If you want to link to an external page, please use this.')

    def __str__(self):
        return self.title

    @property
    def link_location(self):
        return self.link_page.get_absolute_url() if self.link_page else self.link_url

    class Meta:
        abstract = True


class Features(models.Model):
    title = models.CharField(max_length=255, help_text='This is used to help identify the set in the admin')

    class Meta:
        verbose_name_plural = 'Features'

    def __str__(self):
        return self.title


class Feature(models.Model):
    features = models.ForeignKey('components.Features')

    title = models.CharField(max_length=60)
    text = models.TextField(max_length=400)
    image = ImageRefField()

    link_page = models.ForeignKey('pages.Page', blank=True, null=True,
                                  help_text='If you want to link to an internal page, please use this.',
                                  related_name='+')
    link_url = models.CharField(max_length=200, blank=True, null=True,
                                help_text='If you want to link to an external page, please use this.')

    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def link_location(self):
        return self.link_page.get_absolute_url() if self.link_page else self.link_url
