from __future__ import print_function

import urllib.request
from urllib.error import HTTPError

from django.conf import settings
from django.core.management import BaseCommand

from futily.apps.clubs.models import Club
from futily.apps.leagues.models import League
from futily.apps.nations.models import Nation
from futily.apps.players.models import Player


class Command(BaseCommand):
    def handle(self, *args, **options):  # pylint: disable=too-complex
        urls = {
            'nations': 'https://www.easports.com/fifa/ultimate-team/web-app/content/'
                       'B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/images/mobile/flags/list/',
            'leagues': 'https://www.easports.com/fifa/ultimate-team/web-app/content/'
                       'B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/images/mobile/leagueLogos/light/',
            'clubs': 'https://www.easports.com/fifa/ultimate-team/web-app/content/'
                     'B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/images/mobile/clubs/dark/',
            'players': 'https://www.easports.com/fifa/ultimate-team/web-app/content/'
                       'B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/images/mobile/portraits/',
        }

        print('Grabbing Nation images')

        for nation in Nation.objects.all():
            print(f'Getting Nation: {nation}, {nation.ea_id}')

            url = f'{urls["nations"]}{nation.ea_id}.png'
            urllib.request.urlretrieve(url, f'{settings.BASE_ROOT}/futily/static/ea-images/nations/{nation.ea_id}.png')

        print('Grabbing League images')

        for league in League.objects.all():
            print(f'Getting League: {league}')

            url = f'{urls["leagues"]}{league.ea_id}.png'
            urllib.request.urlretrieve(url, f'{settings.BASE_ROOT}/futily/static/ea-images/leagues/{league.ea_id}.png')

        print('Grabbing Club images')

        for club in Club.objects.all():
            print(f'Getting Club: {club}')

            url = f'{urls["clubs"]}{club.ea_id}.png'
            urllib.request.urlretrieve(url, f'{settings.BASE_ROOT}/futily/static/ea-images/clubs/{club.ea_id}.png')

        print('Grabbing Player images')

        for player in Player.objects.all():
            print(f'Getting Player: {player} ({player.ea_id})')

            try:
                url = f'https://www.easports.com/fifa/ultimate-team/web-app/content/B1BA185F-AD7C-4128-8A64' \
                    f'-746DE4EC5A82/2018/fut/playerheads/mobile/single/p{player.ea_id}.png'

                urllib.request.urlretrieve(
                    url,
                    f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                )
            except HTTPError:
                try:
                    url = f'https://www.easports.com/fifa/ultimate-team/web-app/content/B1BA185F-AD7C-4128-8A64' \
                        f'-746DE4EC5A82/2018/fut/playerheads/mobile/single/p{player.ea_id_base}.png'

                    urllib.request.urlretrieve(
                        url,
                        f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                    )
                except HTTPError:
                    try:
                        urllib.request.urlretrieve(
                            f'{urls["players"]}{player.ea_id}.png',
                            f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                        )
                    except HTTPError:
                        urllib.request.urlretrieve(
                            f'{urls["players"]}{player.ea_id_base}.png',
                            f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                        )
            except Exception as e:  # pylint: disable=broad-except
                print(e)
