import json
import urllib.request

from django.conf import settings
from django.core.management import BaseCommand

from six.moves import urllib


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://www.easports.com/uk/fifa/ultimate-team/api/fut/item?jsonParamObject=%7B%22page%22:1%7D'
        total_pages = json.loads(urllib.request.urlopen(url).read())['totalPages']

        for page in range(1, total_pages + 1):
            url = f'https://www.easports.com/uk/fifa/ultimate-team/api/fut/item?jsonParamObject=%7B%22page%22:{page}%7D'
            json_file = f'{settings.BASE_ROOT}/data/players/{page}.json'
            response = urllib.request.urlopen(url)

            with open(json_file, 'wb') as out_file:
                data = response.read()
                out_file.write(data)

                print(out_file)
