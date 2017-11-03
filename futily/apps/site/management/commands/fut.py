import os

import fut
from django.conf import settings
from django.core.management import BaseCommand
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

        print(len(self.f.search('development', level='gold')))
