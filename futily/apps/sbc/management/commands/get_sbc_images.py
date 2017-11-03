import json
import os
import urllib.request

from django.conf import settings
from django.core.management import BaseCommand

from futily.apps.site.management.commands.constants import IMAGE_URLS


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()

        self.challenges_dir = '{}/data/sbcs/challenges'.format(settings.BASE_ROOT)
        self.sets_dir = '{}/data/sbcs/sets'.format(settings.BASE_ROOT)

    def handle(self, *args, **options):
        items = self.get_items()

        for set_data in items['sets']:
            self.get_set_image(set_data)

        for challenge_data in items['challenges']:
            self.get_challenge_image(challenge_data)

    def get_set_image(self, data):
        url = f'{IMAGE_URLS["sbc_set"]}{data["trophyId"]}.png'
        urllib.request.urlretrieve(url, f'{settings.BASE_ROOT}/futily/static/ea-images/sbc/sets/{data["trophyId"]}.png')

    def get_challenge_image(self, data):
        url = f'{IMAGE_URLS["sbc_challenge"]}{data["trophyId"]}.png'
        urllib.request.urlretrieve(
            url, f'{settings.BASE_ROOT}/futily/static/ea-images/sbc/challenges/{data["trophyId"]}.png')

    def get_items(self):
        items = {
            'sets': [],
            'challenges': []
        }
        challenges = os.listdir(self.challenges_dir)
        sets = os.listdir(self.sets_dir)

        for challenge_file in challenges:
            with open(f'{self.challenges_dir}/{challenge_file}', 'r') as open_file:
                try:
                    data = json.load(open_file)
                    items['challenges'].append(data)
                except Exception as e:  # pylint: disable=broad-except
                    print(e)

        for set_file in sets:
            with open(f'{self.sets_dir}/{set_file}', 'r') as open_file:
                try:
                    data = json.load(open_file)
                    items['sets'].append(data)
                except Exception as e:  # pylint: disable=broad-except
                    print(e)

        return items
