from django.core.management import BaseCommand
from django.db.models import Avg, Q

from ....players.constants import QUALITY_TYPES
from ...models import Club


class Command(BaseCommand):
    def handle(self, *args, **options):
        clubs = Club.objects.all()

        for club in clubs:
            players = club.player_set.all()

            # Average rating
            avg = club.average_rating = '{0:.2f}'.format(list(
                players.aggregate(Avg('rating')).values()
            )[0] or 0)

            # All players
            total = club.total_players = len(players)

            # All bronzes
            bronzes = club.total_bronze = players.filter(
                color__in=['bronze', 'rare_bronze']
            ).count()

            # All silvers
            silvers = club.total_silver = players.filter(
                color__in=['silver', 'rare_silver']
            ).count()

            # All golds
            golds = club.total_gold = players.filter(
                color__in=['gold', 'rare_gold']
            ).count()

            # All legends
            legends = club.total_legends = players.filter(
                color__in=QUALITY_TYPES['legend']
            ).count()

            # All TOTW
            totw = club.total_totw = players.filter(
                color__in=QUALITY_TYPES['totw']
            ).count()

            # All special
            special = club.total_special = players.exclude(
                Q(color__in=QUALITY_TYPES['normal']) |
                Q(color__in=QUALITY_TYPES['totw']) |
                Q(color__in=QUALITY_TYPES['legend'])
            ).count()

            club.save()

            print(f'''
                {club.name}

                Average: {avg}
                Total: {total}
                Bronzes: {bronzes}
                Silvers: {silvers}
                Golds: {golds}
                Legends: {legends}
                TOTW's: {totw}
                Specials: {special}
                -----------------------------------''')
