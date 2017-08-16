from cms.admin import PageBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import Type


@admin.register(Type)
class TypeAdmin(SortableModelAdmin, PageBaseAdmin):
    list_display = ['__str__', 'description', 'quality', 'is_online', 'order']
    list_editable = ['quality', 'is_online', 'order']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'page', 'description', 'image'],
        }),
        ('Counts', {
            'fields': ['normal_count', 'rare_count'],
        }),
        ('Roll 1 types', {
            'fields': ['roll_1_types', ('roll_1_types_rating_min', 'roll_1_types_rating_max')],
        }),
        ('Roll 2 types', {
            'fields': ['roll_2_types', ('roll_2_types_rating_min', 'roll_2_types_rating_max')],
        }),
        ('Roll 3 types', {
            'fields': ['roll_3_types', ('roll_3_types_rating_min', 'roll_3_types_rating_max')],
        }),
        ('Roll 4 types', {
            'fields': ['roll_4_types', ('roll_4_types_rating_min', 'roll_4_types_rating_max')],
        }),
        ('Roll 5 types', {
            'fields': ['roll_5_types', ('roll_5_types_rating_min', 'roll_5_types_rating_max')],
        }),
        ('Roll 6 types', {
            'fields': ['roll_6_types', ('roll_6_types_rating_min', 'roll_6_types_rating_max')],
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS
    ]
