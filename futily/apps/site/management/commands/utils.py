import urllib.request
from urllib.error import HTTPError

from django.conf import settings

from futily.apps.site.management.commands.constants import IMAGE_URLS


def get_player_image(player):
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
                    f'{IMAGE_URLS["players"]}{player.ea_id}.png',
                    f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                )
            except HTTPError:
                urllib.request.urlretrieve(
                    f'{IMAGE_URLS["players"]}{player.ea_id_base}.png',
                    f'{settings.BASE_ROOT}/futily/static/ea-images/players/{player.ea_id}.png'
                )
    except Exception as e:  # pylint: disable=broad-except
        print(e)
