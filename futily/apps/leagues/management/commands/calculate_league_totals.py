from django.core.management import BaseCommand
from django.db.models import Avg, Q

from ....players.constants import QUALITY_TYPES
from ...models import League


class Command(BaseCommand):
    def handle(self, *args, **options):
        leagues = League.objects.all()

        for league in leagues:
            players = league.player_set.all()

            # Average rating
            avg = league.average_rating = '{0:.2f}'.format(list(
                players.aggregate(Avg('rating')).values()
            )[0] or 0)

            # All players
            total = league.total_players = len(players)

            # All bronzes
            bronzes = league.total_bronze = players.filter(
                color__in=['bronze', 'rare_bronze']
            ).count()

            # All silvers
            silvers = league.total_silver = players.filter(
                color__in=['silver', 'rare_silver']
            ).count()

            # All golds
            golds = league.total_gold = players.filter(
                color__in=['gold', 'rare_gold']
            ).count()

            # All legends
            legends = league.total_legends = players.filter(
                color__in=QUALITY_TYPES['legend']
            ).count()

            # All TOTW
            totw = league.total_totw = players.filter(
                color__in=QUALITY_TYPES['totw']
            ).count()

            # All special
            special = league.total_special = players.exclude(
                Q(color__in=QUALITY_TYPES['normal']) |
                Q(color__in=QUALITY_TYPES['totw']) |
                Q(color__in=QUALITY_TYPES['legend'])
            ).count()

            league.save()

            print(f'''
                {league.name}

                Average: {avg}
                Total: {total}
                Bronzes: {bronzes}
                Silvers: {silvers}
                Golds: {golds}
                Legends: {legends}
                TOTW's: {totw}
                Specials: {special}
                -----------------------------------''')
