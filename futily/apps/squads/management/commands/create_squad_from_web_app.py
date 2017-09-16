import json
import urllib

from django.core.management import BaseCommand
from django.utils.text import slugify

from futily.apps.players.models import Player
from futily.apps.squads.models import (Squad, SquadPlayer,
                                       get_default_squad_page)
from futily.apps.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://utas.external.s3.fut.ea.com/ut/showofflink/hY69OMXtr2t?timestamp=1503260026849'
        json_data = json.loads(urllib.request.urlopen(url).read())
        squad_data = json_data['data']['squad'][0]
        formation = self.formation_schema(squad_data['formation'])
        players = [
            Player.objects.get(
                ea_id_base=x['itemData']['resourceId']
            ) for x in squad_data['players'] if x['itemData']['resourceId']]
        players = {
            x['index']: {
                'object': Player.objects.get(ea_id_base=x['itemData']['resourceId']),
                'position': x['itemData']['preferredPosition']
            } if x['itemData']['resourceId'] else None for x in squad_data['players']
        }
        title = json_data['squadname']
        web_app_url = json_data['url']

        squad = Squad.objects.create(**{
            'title': title,
            'slug': slugify(title),
            'formation': formation,
            'web_app_import': True,
            'web_app_url': web_app_url,
            'page': get_default_squad_page(),
            'user': User.objects.first(),
        })

        for index, player in players.items():
            if player:
                p = SquadPlayer(player=player['object'], squad=squad, index=index, position=player['position'])
                p.save()

        print(
            f'''
Created: {squad}
            '''
        )

    @staticmethod
    def formation_schema(formation):
        return {
            'f3412': '3412',
            'f3421': '3421',
            'f343': '343',
            'f352': '352',
            'f41212': '41212',
            'f41212a': '41212-2',
            'f4141': '4141',
            'f4222': '4222',
            'f4231': '4231',
            'f4231a': '4231-2',
            'f4312': '4312',
            'f4321': '4321',
            'f433': '433',
            'f433a': '433-2',
            'f433b': '433-3',
            'f433c': '433-4',
            'f433d': '433-5',
            'f4411': '4411',
            'f442': '442',
            'f442a': '442-2',
            'f451': '451',
            'f451a': '451-2',
            'f5212': '5212',
            'f5221': '5221',
            'f532': '532',
        }[formation]
