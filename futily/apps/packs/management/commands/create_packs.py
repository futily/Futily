import urllib
from operator import itemgetter
from xml.etree import ElementTree

from django.core.management import BaseCommand
from django.utils.text import slugify

from ...models import PackType


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://fifa17.content.easports.com/fifa/fltOnlineAssets/CC8267B6-0817-4842-BB6A-A20F88B05418/2017/fut/packs/loc/storepackdescriptions.en_gb.xml'
        res = urllib.request.urlopen(url).read()
        xml = ElementTree.fromstring(res)

        packs = {}

        for child in xml:  # pylint: disable=too-many-nested-blocks
            for child2 in child:
                if child2.tag == 'body':
                    for child3 in child2:
                        name = child3.attrib['resname']

                        if 'FUT_STORE_PACK' in name:
                            pack_id = ''.join([s for s in list(name) if s.isdigit()])

                            if pack_id not in packs:
                                packs[pack_id] = {}

                            if name.endswith('NAME'):
                                packs[pack_id]['name'] = child3.find('source').text

                            if name.endswith('DESC'):
                                packs[pack_id]['description'] = child3.find('source').text

        pack_types = list(map(create_pack_type, packs.items()))
        PackType.objects.bulk_create(pack_types)

        return


def create_pack_type(data):
    key, value = data
    name, description = itemgetter('name', 'description')(value)
    name = name.capitalize()

    if any(x in name for x in ['Epl', 'epl']):
        name = name.replace('Epl', 'EPL')
        name = name.replace('epl', 'EPL')

    if any(x in name for x in ['Fut', 'fut']):
        name = name.replace('Fut', 'FUT')
        name = name.replace('fut', 'FUT')

    if any(x in name for x in ['Mls', 'mls']):
        name = name.replace('Mls', 'MLS')
        name = name.replace('mls', 'MLS')

    if any(x in name for x in ['Sbc', 'sbc']):
        name = name.replace('Sbc', 'SBC')
        name = name.replace('sbc', 'SBC')

    if any(x in name for x in ['Tots', 'tots']):
        name = name.replace('Tots', 'TOTS')
        name = name.replace('tots', 'TOTS')

    if any(x in name for x in ['Tott', 'tott']):
        name = name.replace('Tott', 'TOTT')
        name = name.replace('tott', 'TOTT')

    if any(x in name for x in ['Totw', 'totw']):
        name = name.replace('Totw', 'TOTW')
        name = name.replace('totw', 'TOTW')

    return PackType(**{
        'title': name,
        'slug': slugify(name),
        'description': description,
        'ea_pack': True,
        'ea_id': key,
        'is_online': False,
    })
