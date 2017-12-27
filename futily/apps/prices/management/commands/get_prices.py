import json
from urllib.request import Request, urlopen

import dateparser
from django.core.management import BaseCommand

from futily.apps.players.models import Player, Source
from futily.apps.prices.models import Price


class Command(BaseCommand):
    def handle(self, *args, **options):
        futhead_url = 'http://www.futhead.com/prices/api/?year=18&id={}'
        futbin_url = 'https://www.futbin.com/18/playerPrices?player={}'
        prices = {
            'xbox': [],
            'ps': [],
            'pc': [],
        }
        sources = Source.objects.all()

        for player in Player.objects.filter(source__in=sources):
            print(f'Scraping {player}')
            futhead_req = Request(futhead_url.format(player.ea_id), headers={'User-Agent': 'Mozilla/5.0'})
            futhead_res = json.loads(urlopen(futhead_req).read())

            try:
                for price in futhead_res[str(player.ea_id)]['xbLowFive']:
                    if price > 0:
                        prices['xbox'].append(
                            Price(
                                market='xb',
                                player=player,
                                value=price,
                                source='futhead',
                                last_update=dateparser.parse(str(futhead_res[str(player.ea_id)]['xbTime']))
                            )
                        )
            except Exception as e:
                print(e)

            try:
                for price in futhead_res[str(player.ea_id)]['psLowFive']:
                    if price > 0:
                        prices['ps'].append(
                            Price(
                                market='ps',
                                player=player,
                                value=price,
                                source='futhead',
                                last_update=dateparser.parse(str(futhead_res[str(player.ea_id)]['psTime']))
                            )
                        )
            except Exception as e:
                print(e)

            futbin_req = Request(futbin_url.format(player.ea_id), headers={'User-Agent': 'Mozilla/5.0'})
            futbin_res = json.loads(urlopen(futbin_req).read())
            try:
                for console, obj in futbin_res[str(player.ea_id)]['prices'].items():
                    for key, value in obj.items():
                        if 'LCPrice' in key:
                            price = int(value.replace(',', '') if value else value)

                            if price > 0:
                                prices[console].append(
                                    Price(
                                        market=console if console != 'xbox' else 'xb',
                                        player=player,
                                        value=price,
                                        source='futbin',
                                        last_update=dateparser.parse(futbin_res[str(player.ea_id)]['prices'][console]['updated'])
                                    )
                                )
            except Exception as e:
                print(e)

        prices = [item for sublist in prices.values() for item in sublist]
        Price.objects.bulk_create(prices)
