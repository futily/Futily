from django.core.management import BaseCommand
from django.utils.text import slugify

from futily.utils.list import filter_unique_dict
from ....commands import EaAssetCreatorCommand
from ...models import Nation, get_default_nation_page


class Command(EaAssetCreatorCommand, BaseCommand):
    @staticmethod
    def serialize_nation(nation):
        return {
            'page': get_default_nation_page(),
            'title': nation['name'],
            'slug': slugify(nation['name']),
            'name': nation['name'],
            'name_abbr': nation['abbrName'],
            'ea_id': nation['id'],
        }

    def handle(self, *args, **options):
        items = self.get_items()
        nations = filter_unique_dict([self.get_object(x, 'nation') for x in items], 'id')
        nation_data = list(map(self.serialize_nation, nations))
        nation_instances = [self._create_nation(x) for x in nation_data]

        Nation.objects.bulk_create(nation_instances)

        return

    def _create_nation(self, data):
        return Nation(**data)
