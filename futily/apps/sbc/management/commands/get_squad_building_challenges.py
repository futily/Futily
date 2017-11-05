import json
import os
import time

import fut
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.text import slugify
from dotenv import load_dotenv

dotenv_path = os.path.join(settings.BASE_ROOT, '.env')
load_dotenv(dotenv_path)


class Command(BaseCommand):
    f = None

    def handle(self, *args, **options):
        self.f = fut.Core(
            os.environ.get('EA_EMAIL'),
            os.environ.get('EA_PASSWORD'),
            os.environ.get('EA_SECRET_ANSWER'),
            platform='xbox')

        self.get_challenge_sets()

    def get_challenge_sets(self):
        sets = self.f.sbsSets()

        for category in sets['categories']:
            for cat_set in category['sets']:
                json_file = f'{settings.BASE_ROOT}/data/sbcs/sets/{cat_set["setId"]}-{slugify(cat_set["name"])}.json'
                with open(json_file, 'w') as out_file:
                    out_file.write(json.dumps(cat_set))
                    out_file.close()

                challenges = self.f.sbsSetChallenges(cat_set['setId'])

                print([x['name'] for x in challenges['challenges']])

                for challenge in challenges['challenges']:
                    json_file = f'{settings.BASE_ROOT}/data/sbcs/challenges/{challenge["challengeId"]}-{slugify(challenge["name"])}.json'

                    with open(json_file, 'w') as out_file:
                        out_file.write(json.dumps(challenge))
                        print(out_file)

                    time.sleep(1)
