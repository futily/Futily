import urllib
from operator import itemgetter
from xml.etree import ElementTree

from django.core.management import BaseCommand
from django.utils.text import slugify

from futily.apps.packs.models import PackType, get_default_pack_page
from futily.apps.sbc.models import SquadBuilderChallengeAward


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://fifa18.content.easports.com/fifa/fltOnlineAssets/CC8267B6-0817-4842-BB6A-A20F88B05418/2017/fut/packs/loc/storepackdescriptions.en_gb.xml'
        wanted_ids = [x.value for x in SquadBuilderChallengeAward.objects.filter(type='pack')]
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

                            if int(pack_id) in wanted_ids and pack_id not in packs:
                                packs[pack_id] = {}

                            if int(pack_id) in wanted_ids and name.endswith('NAME'):
                                packs[pack_id]['name'] = child3.find('source').text

                            if int(pack_id) in wanted_ids and name.endswith('DESC'):
                                packs[pack_id]['description'] = child3.find('source').text

        pack_types = list(map(create_pack_type, packs.items()))
        print(pack_types, len(pack_types))
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
        'page': get_default_pack_page(),
        'title': name,
        'slug': slugify(name),
        'description': description,
        'ea_pack': True,
        'ea_id': key,
        'is_online': True,
    })
