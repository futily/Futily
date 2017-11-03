from cms.admin import SearchMetaBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin, SortableTabularInline

from futily.apps.sbc.models import (SquadBuilderChallenge,
                                    SquadBuilderChallengeAward,
                                    SquadBuilderChallengeCategory,
                                    SquadBuilderChallengeRequirement,
                                    SquadBuilderChallengeSet)


@admin.register(SquadBuilderChallengeCategory)
class SquadBuilderChallengeCategoryAdmin(SortableModelAdmin, SearchMetaBaseAdmin):
    prepopulated_fields = {'slug': ['title']}

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'ea_id'],
        }),
        SearchMetaBaseAdmin.PUBLICATION_FIELDS,
        SearchMetaBaseAdmin.SEO_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_TWITTER_FIELDS
    ]


@admin.register(SquadBuilderChallengeSet)
class SquadBuilderChallengeSetAdmin(SortableModelAdmin, SearchMetaBaseAdmin):
    list_display = ['title', 'category', 'end_time', 'is_online']
    list_editable = ['is_online', 'order']

    fieldsets = [
        (None, {
            'fields': ['page', 'category', 'title', 'slug', 'ea_id', 'description', 'end_time'],
        }),
        ('Related', {
            'fields': ['awards'],
        }),
        SearchMetaBaseAdmin.PUBLICATION_FIELDS,
        SearchMetaBaseAdmin.SEO_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_TWITTER_FIELDS
    ]
    filter_horizontal = ['awards']


@admin.register(SquadBuilderChallenge)
class SquadBuilderChallengeAdmin(SearchMetaBaseAdmin):
    list_display = ['set', 'title', 'formation', 'end_time']

    fieldsets = [
        (None, {
            'fields': ['set', 'title', 'slug', 'ea_id', 'formation', 'description', 'end_time',
                       'requirements_operation'],
        }),
        ('Related', {
            'fields': ['awards', 'requirements'],
        }),
        SearchMetaBaseAdmin.PUBLICATION_FIELDS,
        SearchMetaBaseAdmin.SEO_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_TWITTER_FIELDS
    ]
    filter_horizontal = ['awards', 'requirements']
