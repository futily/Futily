from ..constants import POSITION_LINE_MAP
from ..models import get_default_player_page
from ...clubs.models import Club
from ...leagues.models import League
from ...nations.models import Nation


def serialize_player(player):
    print(f'Serialized {player["name"]} ({player["rating"]}) ({player["club"]["name"]})')

    return {
        'page': get_default_player_page(),

        'club': Club.objects.get(ea_id=player['club']['id']),
        'league': League.objects.get(ea_id=player['league']['id']),
        'nation': Nation.objects.get(ea_id=player['nation']['id']),

        'ea_id_base': player['id'],
        'ea_id': player['baseId'],

        'name': player['name'],
        'first_name': player['firstName'],
        'last_name': player['lastName'],
        'common_name': player['commonName'] if player['commonName'] else player['name'],
        'title': player['commonName'] if player['commonName'] else player['name'],

        'image': player['headshotImgUrl'],
        'image_sm': player['headshot']['smallImgUrl'],
        'image_md': player['headshot']['medImgUrl'],
        'image_lg': player['headshot']['largeImgUrl'],
        'image_special_md_totw': player['specialImages']['medTOTWImgUrl'],
        'image_special_lg_totw': player['specialImages']['largeTOTWImgUrl'],

        'position': player['position'],
        'position_full': player['positionFull'],
        'position_line': [k for k, v in POSITION_LINE_MAP.items() if player['position'] in v][0],

        'play_style': player['playStyle'],
        'play_style_id': player['playStyleId'],

        'height': player['height'],
        'weight': player['weight'],
        'birth_date': player['birthdate'],

        'acceleration': player['acceleration'],
        'aggression': player['aggression'],
        'agility': player['agility'],
        'balance': player['balance'],
        'ball_control': player['ballcontrol'],
        'crossing': player['crossing'],
        'curve': player['curve'],
        'dribbling': player['dribbling'],
        'finishing': player['finishing'],
        'free_kick_accuracy': player['freekickaccuracy'],
        'heading_accuracy': player['headingaccuracy'],
        'interceptions': player['interceptions'],
        'jumping': player['jumping'],
        'long_passing': player['longpassing'],
        'long_shots': player['longshots'],
        'marking': player['marking'],
        'penalties': player['penalties'],
        'positioning': player['positioning'],
        'potential': player['potential'],
        'reactions': player['reactions'],
        'short_passing': player['shortpassing'],
        'shot_power': player['shotpower'],
        'sliding_tackle': player['slidingtackle'],
        'sprint_speed': player['sprintspeed'],
        'standing_tackle': player['standingtackle'],
        'stamina': player['stamina'],
        'strength': player['strength'],
        'vision': player['vision'],
        'volleys': player['volleys'],

        'gk_diving': player['gkdiving'],
        'gk_handling': player['gkhandling'],
        'gk_kicking': player['gkkicking'],
        'gk_positioning': player['gkpositioning'],
        'gk_reflexes': player['gkreflexes'],

        'foot': player['foot'],
        'skill_moves': player['skillMoves'],
        'weak_foot': player['weakFoot'],

        'card_att_1': player['attributes'][0]['value'],
        'card_att_2': player['attributes'][1]['value'],
        'card_att_3': player['attributes'][2]['value'],
        'card_att_4': player['attributes'][3]['value'],
        'card_att_5': player['attributes'][4]['value'],
        'card_att_6': player['attributes'][5]['value'],
        'rating': player['rating'],

        'specialities': player['specialities'],
        'traits': player['traits'],

        'work_rate_att': player['atkWorkRate'],
        'work_rate_def': player['defWorkRate'],

        'player_type': player['playerType'],
        'item_type': player['itemType'],
        'model_name': player['modelName'],
        'quality': player['quality'],
        'color': player['color'],

        'is_gk': player['isGK'],
        'is_special_type': player['isSpecialType'],
    }
