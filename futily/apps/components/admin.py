from django.contrib import admin
from suit.admin import SortableStackedInline

from ...utils.admin import UsedOnAdminMixin
from .models import Feature, Features


class FeatureAdmin(SortableStackedInline):
    model = Feature
    extra = 0

    class Media:
        css = {
            'all': ['/static/css/admin-sections.css'],
        }


@admin.register(Features)
class FeaturesAdmin(UsedOnAdminMixin, admin.ModelAdmin):
    inlines = [FeatureAdmin]
