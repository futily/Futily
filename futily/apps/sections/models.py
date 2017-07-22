from __future__ import print_function

from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, Page
from cms.models import HtmlField
from django.db import models
from django.shortcuts import render_to_response
from django.utils.text import slugify

from ..players.models import Player, Source

SECTION_TYPES = (
    ('Adverts', {
        'sections': [
            ('728x90', {
                'fields': [],
            }),
        ]
    }),
    ('Content', {
        'sections': [
            ('features', {
                'fields': ['title', 'text', 'features'],
            }),
            ('search', {
                'fields': ['title', 'text'],
            }),
            ('special-teams', {
                'fields': [],
            }),
        ]
    }),
)


def get_section_name(obj):
    if 'name' in obj[1]:
        return obj[1]['name']

    return obj[0][0].upper() + obj[0][1:].replace('-', ' ')


def sections_js(request):
    model_fields = SectionBase._meta.get_fields()
    # Since our sections aren't at the top level we'll need to create an array
    # of them when we are iterating
    sections = []

    # Each optgroup we define
    for group in SECTION_TYPES:
        # Every section that appears in the optgroup
        for section_type in group[1]['sections']:
            fields = section_type[1].get('fields', [])

            # We've got a section so lets add it to the sections list
            sections.append({
                'name': section_type[0],
                'fields': fields
            })

            for field in fields:
                if field not in model_fields:
                    print(f"NOTE: Field `{field}` is referenced by section type `{section_type[0]}`, but doesn't exist.")

    return render_to_response('admin/pages/page/sections.js', {
        'types': sections,
    }, content_type='application/javascript')


def get_section_type_choices(types):
    # Will be used to build up our optgroups
    groups = []

    for section_group in SECTION_TYPES:
        label = section_group[0]
        content = section_group[1]

        # We'll need to build a tuple of the section option value & option name
        sections = []

        for section in content['sections']:
            section_label = section[0]

            sections.append((slugify(section_label), get_section_name(section)))

        groups.append((label, sections))

    return groups


class SectionBase(models.Model):
    page = models.ForeignKey(Page)
    type = models.CharField(choices=get_section_type_choices(SECTION_TYPES), max_length=100)

    title = models.CharField(max_length=140, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    content = HtmlField(blank=True, null=True)
    image = ImageRefField(blank=True, null=True)

    features = models.ForeignKey('components.Features', blank=True, null=True)

    order = models.PositiveIntegerField(default=0, help_text='Order which the section will be displayed')

    class Meta:
        abstract = True
        ordering = ('order',)

    def __str__(self):
        return dict(SECTION_TYPES)[self.type]['name']

    @property
    def template(self):
        return self.type + '.html'

    @staticmethod
    def get_special_teams():
        latest_totw = Source.objects.filter(short_title__contains='34')[0]
        latest_tots = Source.objects.filter(short_title__contains='TOTS Gold')[0]

        return {
            'latest': {
                'players': Player.objects.order_by('-created')[:8],
                'link': '#'
            },
            'tots': {
                'players': Player.objects.filter(source=latest_tots)[:8],
                # 'link': Squad.objects.get(title=latest_tots.title, is_special=True)
            },
            'totw': {
                'players': Player.objects.filter(source=latest_totw)[:8],
                # 'link': Squad.objects.get(title=latest_totw.title, is_special=True)
            },
        }


class ContentSection(SectionBase):

    def __str__(self):
        return self.type.capitalize()


class Content(ContentBase):

    def __str__(self):
        return self.page.title
