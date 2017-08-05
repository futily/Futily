from django.core.management import BaseCommand
from django.utils.text import slugify

from futily.utils.list import filter_unique_dict, find_dict_by_value

from ....commands import EaAssetCreatorCommand
from ....nations.models import Nation, get_default_nation_page
from ...models import League, get_default_league_page


class Command(EaAssetCreatorCommand, BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

        self.legend_nation = {}

    @staticmethod
    def serialize_league(league):
        return {
            'page': get_default_league_page(),
            'title': league['name'],
            'slug': slugify(league['name']),
            'name': league['name'],
            'name_abbr': league['abbrName'],
            'ea_id': league['id'],
        }

    def handle(self, *args, **options):
        items = self.get_items()
        leagues = filter_unique_dict([self.get_object(x, 'league') for x in items], 'id')
        league_data = list(map(self.serialize_league, leagues))
        team_config = self.get_team_config()

        for league in league_data:
            try:
                nation_id = find_dict_by_value(
                    team_config['Leagues'], 'LeagueId', league['ea_id']
                )['NationId']
                nation = Nation.objects.get(ea_id=nation_id)
            except Exception:  # pylint: disable=broad-except
                if league['name'] == 'Legends':
                    nation_id = find_dict_by_value(
                        team_config['LegendsLeagues'], 'LeagueId', league['ea_id']
                    )['NationId']
                    self.legend_nation = {
                        'page': get_default_nation_page(),
                        'name': 'Legends',
                        'name_abbr': 'Legends',
                        'ea_id': nation_id,
                        'slug': 'legends',
                    }
                    nation, created = Nation.objects.get_or_create(**self.legend_nation)  # pylint: disable=unused-variable

            league['nation'] = nation

        league_instances = [self._create_league(x) for x in league_data]
        League.objects.bulk_create(league_instances)

        return

    def _create_league(self, data):
        return League(**data)
