import json
import os
import urllib.request

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.text import slugify

from futily.apps.clubs.models import Club
from futily.apps.leagues.models import League
from futily.apps.nations.models import Nation
from futily.apps.players.management.commands.create_players import \
    serialize_player
from futily.apps.players.models import Player
from futily.apps.sbc.models import (SquadBuilderChallenge,
                                    SquadBuilderChallengeAward,
                                    SquadBuilderChallengeCategory,
                                    SquadBuilderChallengeRequirement,
                                    SquadBuilderChallengeSet,
                                    get_default_sbc_page)
from futily.apps.site.management.commands.utils import get_player_image


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

        self.challenges_dir = '{}/data/sbcs/challenges'.format(settings.BASE_ROOT)
        self.sets_dir = '{}/data/sbcs/sets'.format(settings.BASE_ROOT)

    def handle(self, *args, **options):
        items = self.get_items()

        for set_data in items['sets']:
            self.build_sets(set_data)

        for challenge_data in items['challenges']:
            self.build_challenges(challenge_data)

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

    def build_challenges(self, data):
        sbc_challenge, created = SquadBuilderChallenge.objects.get_or_create(
            set=SquadBuilderChallengeSet.objects.get(ea_id=data['setId']),
            title=data['name'],
            slug=slugify(data['name']),
            description=data['description'],
            ea_id=data['challengeId'],
            trophy_id=data['trophyId'],
            order=data['priority'],
            formation=FORMATION_SCHEMA[data['formation']],
            # All of them are 'AND' so far
            requirements_operation='AND',
        )
        sbc_challenge.save()
        print(sbc_challenge, created)

        if 'awards' in data:
            awards = self.build_awards(data['awards'])
            sbc_challenge.awards.add(*awards)
            print(sbc_challenge.awards)

        print(data['name'], SquadBuilderChallengeSet.objects.get(ea_id=data['setId']))
        requirements = self.build_requirements(data['elgReq'])
        sbc_challenge.requirements.add(*requirements)
        print(sbc_challenge.requirements)

    def build_sets(self, data):
        sbc_set, created = SquadBuilderChallengeSet.objects.get_or_create(
            page=get_default_sbc_page(),
            ea_id=data['setId'],
            trophy_id=data['trophyId'],
            title=data['name'],
            slug=slugify(data['name']),
            description=data['description'],
            order=data['priority'],
            category=SquadBuilderChallengeCategory.objects.get(ea_id=data['categoryId'])
        )
        sbc_set.save()

        print(sbc_set, created)

        awards = self.build_awards(data['awards'])
        sbc_set.awards.add(*awards)
        print(sbc_set.awards)

    def build_awards(self, award_data):
        awards = []

        for award in award_data:
            sbc_award, created = SquadBuilderChallengeAward.objects.get_or_create(
                type=award['type'],
                value=award['value'],
                hal_id=award['halId'],
                player=self.get_or_create_player(award) if award['type'] == 'item' else None,
                is_untradeable=award['isUntradeable'],
            )
            awards.append(sbc_award)
            print(sbc_award, created)

        return awards

    @staticmethod
    def build_requirements(requirement_data):
        requirements = []

        for requirement in requirement_data:
            slot = requirement['eligibilitySlot'] - 1

            try:
                key = requirements[slot]
            except IndexError:
                requirements.append([])
                key = requirements[slot]

            if requirement['type'] == 'SCOPE':
                key.append(('SCOPE', SCOPE_SCHEMA[requirement['eligibilityValue']]))
            else:
                value = requirement['eligibilityValue']

                if requirement['type'] == 'NATION_ID':
                    value = Nation.objects.get(ea_id=requirement['eligibilityValue'])
                elif requirement['type'] == 'LEAGUE_ID':
                    value = League.objects.get(ea_id=requirement['eligibilityValue'])
                elif requirement['type'] == 'CLUB_ID':
                    value = Club.objects.get(ea_id=requirement['eligibilityValue'])
                elif requirement['type'] == 'PLAYER_LEVEL' or requirement['type'] == 'PLAYER_QUALITY':
                    value = LEVEL_SCHEMA[requirement['eligibilityValue']]
                elif requirement['type'] == 'PLAYER_RARITY':
                    value = RARITY_SCHEMA[requirement['eligibilityValue']]

                key.append((requirement['type'], value))

        requirement_objs = []

        for requirement in requirements:
            obj = {}

            for req_type, value in requirement:
                if req_type == 'SCOPE':
                    obj['scope'] = value
                elif req_type == 'NATION_ID':
                    obj['nation'] = value
                elif req_type == 'LEAGUE_ID':
                    obj['league'] = value
                elif req_type == 'CLUB_ID':
                    obj['club'] = value
                elif req_type == 'PLAYER_LEVEL' or req_type == 'PLAYER_QUALITY':
                    obj['player_quality'] = value
                elif req_type == 'PLAYER_RARITY':
                    obj['player_rarity'] = value
                else:
                    obj['type'] = req_type
                    obj['type_value'] = value

            req, created = SquadBuilderChallengeRequirement.objects.get_or_create(**obj)
            requirement_objs.append(req)
            print(req, created)

        return requirement_objs

    @staticmethod
    def get_or_create_player(data):
        item_data = data['itemData']
        ea_id = item_data['id']
        ea_id_base = item_data['assetId']

        try:
            return Player.objects.get(ea_id=ea_id)
        except Player.DoesNotExist:
            url = f'https://www.easports.com/fifa/ultimate-team/api/fut/item?jsonParamObject={{"baseid":"{ea_id_base}","link":1}}'
            response = urllib.request.urlopen(url)
            json_data = json.loads(response.read())

            for item in json_data['items']:
                if int(item['id']) != int(ea_id):
                    continue

                player = Player.objects.get_or_create(**serialize_player(item))
                get_player_image(player)

                return player


FORMATION_SCHEMA = {
    'f3412': '3412',
    'f3421': '3421',
    'f343': '343',
    'f352': '352',
    'f41212': '41212',
    'f41212a': '41212-2',
    'f4141': '4141',
    'f4231': '4231',
    'f4231a': '4231-2',
    'f4222': '4222',
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
}

LEVEL_SCHEMA = {
    1: 'bronze',
    2: 'silver',
    3: 'gold',
}

RARITY_SCHEMA = {
    1: 'rare',
    3: 'inform',
    12: 'legend',
}

SCOPE_SCHEMA = {
    0: 'gte',
    1: 'lte',
    2: 'exact',
}

'''
enums.SBC.CHALLENGE_TYPE = {
    OPEN: "OPEN_CHALLENGE",
    BRICK: "BRICK_CHALLENGE",
    CUSTOM_BRICK: "CUSTOM_BRICK_CHALLENGE"
},
enums.SBC.PLAYER_TYPE = {
    DEFAULT: "DEFAULT",
    BRICK: "BRICK",
    CUSTOM_BRICK: "CUSTOM_BRICK"
},
enums.SBC.ELG_OPERATION = {
    AND: "AND",
    OR: "OR"
},
enums.SBC.ELG_KEY = {
    FUT_ELGRULE_TEAM_STAR_RATING: 0,
    FUT_ELGRULE_TEAM_CHEMISTRY: 1,
    FUT_ELGRULE_PLAYER_COUNT: 2,
    FUT_ELGRULE_PLAYER_QUALITY: 3,
    FUT_ELGRULE_SAME_NATION_COUNT: 4,
    FUT_ELGRULE_SAME_LEAGUE_COUNT: 5,
    FUT_ELGRULE_SAME_CLUB_COUNT: 6,
    FUT_ELGRULE_NATION_COUNT: 7,
    FUT_ELGRULE_LEAGUE_COUNT: 8,
    FUT_ELGRULE_CLUB_COUNT: 9,
    FUT_ELGRULE_NATION_ID: 10,
    FUT_ELGRULE_LEAGUE_ID: 11,
    FUT_ELGRULE_CLUB_ID: 12,
    FUT_ELGRULE_SCOPE: 13,
    FUT_ELGRULE_APPLY_TO: 14,
    FUT_ELGRULE_LEGEND_COUNT: 15,
    FUT_ELGRULE_NUM_TROPHY_REQUIRED: 16,
    FUT_ELGRULE_PLAYER_LEVEL: 17,
    FUT_ELGRULE_PLAYER_RARITY: 18,
    FUT_ELGRULE_TEAM_RATING: 19,
    FUT_ELGRULE_PLAYER_COUNT_COMBINED: 21
},
enums.SBC.ELG_SCOPE = {
    FUT_ELGRULE_SCOPE_GREATER: 0,
    FUT_ELGRULE_SCOPE_LOWER: 1,
    FUT_ELGRULE_SCOPE_EXACT: 2
},
enums.SBC.ELG_QUALITY_TYPES = {
    BRONZE: 1,
    SILVER: 2,
    GOLD: 3
},
'''
