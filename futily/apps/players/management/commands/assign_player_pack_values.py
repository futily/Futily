from django.core.management import BaseCommand

from futily.apps.players.models import Player


class Command(BaseCommand):
    color_schema = {
        'bronze': 14,
        'rare_bronze': 38,
        'silver': 98,
        'rare_silver': 228,
        'gold': 300,
        'rare_gold': 650,
        'totw_silver': 4550,
        'totw_gold': 9150,
        'ones_to_watch': 9150,
        'halloween': 9150,
        'legend': 102000,
    }
    rating_schema = {
        'bronze': 1,
        'rare_bronze': 1,
        'silver': 1,
        'rare_silver': 3,
        'gold': 4,
        'rare_gold': 8,
        'totw_silver': 70,
        'totw_gold': 122,
        'ones_to_watch': 122,
        'halloween': 122,
        'legend': 1200,
    }

    def handle(self, *args, **options):
        players = Player.objects.all()

        for player in players:
            player.pack_value = self.color_schema[player.color] +\
                (player.rating * self.rating_schema[player.color]) +\
                round(player.total_ingame_stats / 10)
            print(f'<{player} (player.rating)> Value: {player.pack_value}')
            player.save()
