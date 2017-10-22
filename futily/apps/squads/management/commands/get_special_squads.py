import json

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from futily.apps.players.management.commands.create_players import \
    serialize_player
from futily.apps.players.models import Player, Source
from futily.apps.site.management.commands.utils import get_player_image
from futily.apps.squads.models import Squad, SquadPlayer, Squads
from futily.apps.users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('squad_id', nargs='+', type=str)

    def handle(self, *args, **options):  # pylint: disable=too-many-locals
        squad_id = options['squad_id'][0]
        url = 'https://www.easports.com/fifa/ultimate-team/fut/team/18/{}'.format(squad_id)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        script_tags = soup.find_all('script')

        for tag in script_tags:
            if "angular.module('totx').value('squadData'," in tag.text:
                data = tag.text.split('\n')[1].replace(
                    '    angular.module(\'totx\').value(\'squadData\', ', '').replace(');', '')

                data_json = json.loads(data)

                title = data_json['displayName']
                short_title = data_json['name']
                players = data_json['players']

                source, created = Source.objects.get_or_create(title=title, short_title=short_title, ea_url=url)
                player_data = list(map(serialize_player, players))
                player_objects = []

                for player in player_data:
                    player['source'] = source

                for player in player_data:
                    try:
                        obj = Player.objects.get(ea_id=player['ea_id'])
                        created = False
                    except Player.DoesNotExist:
                        obj = Player.objects.create(**player)
                        obj.save()

                        created = True

                    player_objects.append(obj)

                    print(u'{} player: {}'.format('Created' if created else 'Found', obj.name))

                    get_player_image(obj)

                try:
                    squad = Squad.objects.get(title=title, is_special=True)
                except Squad.DoesNotExist:
                    squad = Squad.objects.create(
                        title=title,
                        short_title=short_title,
                        page=Squads.objects.first(),
                        formation=data_json['formationId'].replace('f', ''),
                        is_special=True,
                        small_image_url=f'http{data_json["squadImageSmall"]}',
                        large_image_url=f'http{data_json["squadImageLarge"]}',
                        description=data_json['description'],
                        user=User.objects.first(),
                    )
                    squad.save()

                    for index, player in enumerate(player_objects):
                        p = SquadPlayer(player=player, squad=squad, index=index, position=player.position)
                        p.save()

                    ratings = [x.player.rating for x in squad.players.all()]
                    squad.rating = round(sum(ratings) / len(ratings))
                    squad.save()

                print('{} created: {}'.format(squad.title, squad.get_absolute_url()))
