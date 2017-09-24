from cms.admin import PageBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .forms import PackTypeAdmin
from .models import PackType


@admin.register(PackType)
class TypeAdmin(SortableModelAdmin, PageBaseAdmin):
    form = PackTypeAdmin
    list_display = ['__str__', 'description', 'type', 'is_online', 'order']
    list_editable = ['type', 'description', 'is_online', 'order']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'page', 'description', 'type'],
        }),
        ('Counts', {
            'fields': ['bronze_count', 'silver_count', 'gold_count', 'rare_count', 'total_count'],
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS
    ]
