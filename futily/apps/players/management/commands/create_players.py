from __future__ import print_function

from django.core.management import BaseCommand

from futily.apps.players.utils.management import serialize_player

from ....commands import EaAssetCreatorCommand
from ...models import Player


class Command(EaAssetCreatorCommand, BaseCommand):
    def handle(self, *args, **options):
        players = self.get_items()
        player_data = list(map(serialize_player, players))
        player_instances = [self._create_player(x) for x in player_data]

        Player.objects.bulk_create(player_instances, batch_size=100)

        return

    def _create_player(self, data):
        return Player(**data)
