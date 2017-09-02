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
    def handle(self, *args, **options):
        urls = {
            'nations': 'https://fifa17.content.easports.com/fifa/fltOnlineAssets/CC8267B6-0817-4842-BB6A-A20F88B05418'
                       '/2017/fut/items/images/flags/web/high/',
            'leagues': 'https://fifa17.content.easports.com/fifa/fltOnlineAssets/CC8267B6-0817-4842-BB6A-A20F88B05418'
                       '/2017/fut/items/images/leagueLogos_sm/web/light/l',
            'clubs': 'https://fifa17.content.easports.com/fifa/fltOnlineAssets/CC8267B6-0817-4842-BB6A-A20F88B05418'
                     '/2017/fut/items/images/clubbadges/web/normal/s',
            'players': 'https://fifa17.content.easports.com/fifa/fltOnlineAssets/CC8267B6-0817-4842-BB6A-A20F88B05418'
                       '/2017/fut/items/images/players/html5/120x120/{}.png',
        }

        print('Grabbing Nation images')

        for nation in Nation.objects.all():
            print(f'Getting Nation: {nation}')

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
            print(f'Getting Player: {player} ({player.ea_id_base})')

            try:
                urllib.request.urlretrieve(
                    urls['players'].format(player.ea_id),
                    f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                )
            except HTTPError:
                urllib.request.urlretrieve(
                    f'https://fifa17.content.easports.com/fifa/fltOnlineAssets/CC8267B6-0817-4842-BB6A-A20F88B05418/2017/fut/items/images/players/web/{player.ea_id}.png',
                    f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                )
            except Exception as e:  # pylint: disable=broad-except
                print(e)
