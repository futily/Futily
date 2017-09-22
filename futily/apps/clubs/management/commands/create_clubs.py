from __future__ import print_function

from django.core.management import BaseCommand
from django.utils.text import slugify

from futily.utils.list import filter_unique_dict, find_dict_by_value

from ....commands import EaAssetCreatorCommand
from ....leagues.models import League
from ...models import Club, get_default_club_page


class Command(EaAssetCreatorCommand, BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

        self.legend_nation = {}

    @staticmethod
    def serialize_club(club):
        return {
            'page': get_default_club_page(),
            'title': club['name'],
            'slug': slugify(club['name']),
            'name': club['name'],
            'name_abbr': club['abbrName'],
            'ea_id': club['id'],
        }

    def handle(self, *args, **options):
        items = self.get_items()
        clubs = filter_unique_dict([self.get_object(x, 'club') for x in items], 'id')
        club_data = list(map(self.serialize_club, clubs))
        team_config = self.get_team_config()

        for club in club_data:
            try:
                league_id = find_dict_by_value(
                    team_config['Teams'], 'TeamId', club['ea_id']
                )['LeagueId']
                league = League.objects.get(ea_id=league_id)
            except Exception:  # pylint: disable=broad-except
                if club['name'] == 'Legends' or club['name'] == 'Icons':
                    league_id = find_dict_by_value(
                        team_config['LegendsTeams'], 'TeamId', club['ea_id']
                    )['LeagueId']
                    league = League.objects.get(ea_id=league_id)

            club['league'] = league

        club_instances = [self._create_club(x) for x in club_data]
        Club.objects.bulk_create(club_instances, batch_size=50)

        return

    def _create_club(self, data):
        return Club(**data)
