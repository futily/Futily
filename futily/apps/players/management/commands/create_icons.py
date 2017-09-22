from __future__ import print_function

from django.core.management import BaseCommand

from futily.apps.commands import EaAssetCreatorCommand
from futily.apps.players.models import Icon, Player


class Command(EaAssetCreatorCommand, BaseCommand):
    def handle(self, *args, **options):
        players = self.get_items()

        for player in players:
            if player['iconAttributes']:
                icon = Icon.objects.create(
                    player=Player.objects.get(ea_id=player['id']),
                    club_team_stats=player['iconAttributes']['clubTeamStats'],
                    national_team_stats=player['iconAttributes']['nationalTeamStats'],
                    text=player['iconAttributes']['iconText'],
                )

                print(f'Created Icon for {icon.player.__str__()}')

        return
