import json
from urllib.request import Request, urlopen

import dateparser
from django.core.management import BaseCommand

from futily.apps.players.models import Player, Source
from futily.apps.prices.models import Price


class Command(BaseCommand):
    def handle(self, *args, **options):
        futbin_prices = self.scrape_futbin()
        futhead_prices = self.scrape_futhead()
        prices = futbin_prices + futhead_prices

        Price.objects.bulk_create(prices)

    def scrape_futhead(self):
        url = 'http://www.futhead.com/prices/api/?year=18&id={}'
        sources = Source.objects.all()

        prices = {
            'xbox': [],
            'ps': [],
            'pc': [],
        }

        for player in Player.objects.filter(source__in=sources):
            req = Request(url.format(player.ea_id), headers={'User-Agent': 'Mozilla/5.0'})
            res = json.loads(urlopen(req).read())

            for price in res[str(player.ea_id)]['xbLowFive']:
                prices['xbox'].append(
                    Price(
                        market='xb',
                        player=player,
                        value=price,
                        source='futhead',
                        last_update=dateparser.parse(str(res[str(player.ea_id)]['xbTime']))
                    )
                )

            for price in res[str(player.ea_id)]['psLowFive']:
                prices['ps'].append(
                    Price(
                        market='ps',
                        player=player,
                        value=price,
                        source='futhead',
                        last_update=dateparser.parse(str(res[str(player.ea_id)]['psTime']))
                    )
                )

        return [item for sublist in prices.values() for item in sublist]

    def scrape_futbin(self):
        url = 'https://www.futbin.com/18/playerPrices?player={}'
        sources = Source.objects.all()

        prices = {
            'xbox': [],
            'ps': [],
            'pc': [],
        }

        for player in Player.objects.filter(source__in=sources):
            req = Request(url.format(player.ea_id), headers={'User-Agent': 'Mozilla/5.0'})
            res = json.loads(urlopen(req).read())

            for console, obj in res[str(player.ea_id)]['prices'].items():
                for key, value in obj.items():
                    if 'LCPrice' in key:
                        prices[console].append(
                            Price(
                                market=console if console != 'xbox' else 'xb',
                                player=player,
                                value=int(value.replace(',', '') if value else value),
                                source='futbin',
                                last_update=dateparser.parse(res[str(player.ea_id)]['prices'][console]['updated'])
                            )
                        )

        return [item for sublist in prices.values() for item in sublist]
