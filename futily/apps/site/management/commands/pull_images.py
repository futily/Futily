from __future__ import print_function

import urllib.request

from django.conf import settings
from django.core.management import BaseCommand

from futily.apps.clubs.models import Club
from futily.apps.leagues.models import League
from futily.apps.nations.models import Nation
from futily.apps.players.models import Player
from futily.apps.site.management.commands.constants import IMAGE_URLS
from futily.apps.site.management.commands.utils import get_player_image


class Command(BaseCommand):
    def handle(self, *args, **options):  # pylint: disable=too-complex
        print('Grabbing Nation images')

        for nation in Nation.objects.all():
            print(f'Getting Nation: {nation}, {nation.ea_id}')

            url = f'{IMAGE_URLS["nations"]}{nation.ea_id}.png'
            urllib.request.urlretrieve(url, f'{settings.BASE_ROOT}/futily/static/ea-images/nations/{nation.ea_id}.png')

        print('Grabbing League images')

        for league in League.objects.all():
            print(f'Getting League: {league}')

            url = f'{IMAGE_URLS["leagues"]}{league.ea_id}.png'
            urllib.request.urlretrieve(url, f'{settings.BASE_ROOT}/futily/static/ea-images/leagues/{league.ea_id}.png')

        print('Grabbing Club images')

        for club in Club.objects.all():
            print(f'Getting Club: {club}')

            url = f'{IMAGE_URLS["clubs"]}{club.ea_id}.png'
            urllib.request.urlretrieve(url, f'{settings.BASE_ROOT}/futily/static/ea-images/clubs/{club.ea_id}.png')

        print('Grabbing Player images')

        for player in Player.objects.all():
            get_player_image(player)
