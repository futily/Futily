from django.core.management import BaseCommand
from django.db.models import Avg, Q

from ....players.constants import QUALITY_TYPES
from ...models import Nation


class Command(BaseCommand):
    def handle(self, *args, **options):
        nations = Nation.objects.all()

        for nation in nations:
            players = nation.player_set.all()

            # Average rating
            avg = nation.average_rating = '{0:.2f}'.format(list(
                players.aggregate(Avg('rating')).values()
            )[0] or 0)

            # All players
            total = nation.total_players = len(players)

            # All bronzes
            bronzes = nation.total_bronze = players.filter(
                color__in=['bronze', 'rare_bronze']
            ).count()

            # All silvers
            silvers = nation.total_silver = players.filter(
                color__in=['silver', 'rare_silver']
            ).count()

            # All golds
            golds = nation.total_gold = players.filter(
                color__in=['gold', 'rare_gold']
            ).count()

            # All legends
            legends = nation.total_legends = players.filter(
                color__in=QUALITY_TYPES['legend']
            ).count()

            # All TOTW
            totw = nation.total_totw = players.filter(
                color__in=QUALITY_TYPES['totw']
            ).count()

            # All special
            special = nation.total_special = players.exclude(
                Q(color__in=QUALITY_TYPES['normal']) |
                Q(color__in=QUALITY_TYPES['totw']) |
                Q(color__in=QUALITY_TYPES['legend'])
            ).count()

            nation.save()

            print(
                f'''
                {nation.name}

                Average: {avg}
                Total: {total}
                Bronzes: {bronzes}
                Silvers: {silvers}
                Golds: {golds}
                Legends: {legends}
                TOTW's: {totw}
                Specials: {special}
                -----------------------------------'''
            )
