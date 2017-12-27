BASE_COLOR_CHOICES = [
    ('bronze', 'Bronze'),
    ('silver', 'Silver'),
    ('gold', 'Gold'),
    ('rare_bronze', 'Rare bronze'),
    ('rare_silver', 'Rare silver'),
    ('rare_gold', 'Rare gold'),
    ('legend', 'Legend'),
]

SPECIAL_COLOR_CHOICES = [
    ('award_winner', 'Award Winner'),
    ('confederation_champions_motm', 'Confederation Champions MOTM'),
    ('europe_motm', 'Europe MOTM'),
    ('fut_birthday', 'FUT Birthday'),
    ('fut_champions_bronze', 'FUT Champions Bronze'),
    ('fut_champions_gold', 'FUT Champions Gold'),
    ('fut_champions_silver', 'FUT Champions Silver'),
    ('fut_championship', 'FUT Championship'),
    ('fut_mas', 'FUT Mas'),
    ('fut_united', 'FUT United'),
    ('futties_winner', 'Futties Winner'),
    ('gotm', 'GOTM'),
    ('halloween', 'Halloween'),
    ('imotm', 'iMOTM'),
    ('marquee', 'Marquee'),
    ('motm', 'MOTM'),
    ('movember', 'Movember'),
    ('ones_to_watch', 'Ones To Watch'),
    ('pink', 'Pink'),
    ('purple', 'Purple'),
    ('record_breaker', 'Record Breaker'),
    ('rtr_contender', 'RTR Contender'),
    ('rtr_gold', 'RTR Gold'),
    ('sbc_base', 'SBC Base'),
    ('sbc_premium', 'SBC Premium'),
    ('st_patricks', 'St. Patricks'),
    ('teal', 'teal'),
    ('tots_bronze', 'TOTS Bronze'),
    ('tots_gold', 'TOTS Gold'),
    ('tots_silver', 'TOTS Silver'),
    ('totw_bronze', 'TOTW Bronze'),
    ('totw_gold', 'TOTW Gold'),
    ('totw_silver', 'TOTW Silver'),
    ('toty', 'TOTY'),
]

LEVEL_FILTER_MAP = {
    'TOTW': ['totw_bronze', 'totw_silver', 'totw_gold'],
    'GOLD': ['gold', 'rare_gold', 'totw_gold'],
    'SILVER': ['silver', 'rare_silver', 'totw_silver'],
    'BRONZE': ['bronze', 'rare_bronze', 'totw_bronze'],
    'TOTW-GOLD': ['totw_gold'],
    'TOTW-SILVER': ['totw_silver'],
    'TOTW-BRONZE': ['totw_bronze'],
    'RARE-GOLD': ['rare_gold'],
    'RARE-SILVER': ['rare_silver'],
    'RARE-BRONZE': ['rare_bronze'],
    'NONRARE-GOLD': ['gold'],
    'NONRARE-SILVER': ['silver'],
    'NONRARE-BRONZE': ['bronze'],
    'LEGEND': ['legend'],
    'TOTY': ['toty'],
    'MOTM': ['motm', 'imotm'],
    'TRANSFERS': [''],
    'SPECIAL': ['ones_to_watch', 'fut_champions_bronze', 'fut_champions_silver', 'fut_champions_gold',
                'sbc_base', 'halloween', 'movember', 'award_winner', 'confederation_champions_motm',
                'gotm', 'st_patricks', 'fut_birthday', 'tots_bronze', 'tots_silver', 'tots_gold', 'pink',
                'futties_winner'],
}

LEVELS_GET_TO_LABEL = {
    value: key
    for (value, key) in BASE_COLOR_CHOICES + SPECIAL_COLOR_CHOICES
}

POSITION_CHOICES = [
    ('GK', 'GK'),
    ('RWB', 'RWB'),
    ('RB', 'RB'),
    ('CB', 'CB'),
    ('LB', 'LB'),
    ('LWB', 'LWB'),
    ('CDM', 'CDM'),
    ('CM', 'CM'),
    ('CAM', 'CAM'),
    ('RM', 'RM'),
    ('RW', 'RW'),
    ('RF', 'RF'),
    ('LM', 'LM'),
    ('LW', 'LW'),
    ('LF', 'LF'),
    ('CF', 'CF'),
    ('ST', 'ST'),
]

POSITION_GET_TO_LABEL = {
    'all': 'All positions',
    'gk': 'Goalkeepers',
    'def': 'Defenders',
    'mid': 'Midfielders',
    'att': 'Attackers',
    'rwb': 'RWB',
    'rb': 'RB',
    'cb': 'CB',
    'lb': 'LB',
    'lwb': 'LWB',
    'cdm': 'CDM',
    'cm': 'CM',
    'cam': 'CAM',
    'rm': 'RM',
    'rw': 'RW',
    'rf': 'RF',
    'lm': 'LM',
    'lw': 'LW',
    'lf': 'LF',
    'cf': 'CF',
    'st': 'ST',
    'cbs': 'Center backs',
    'rbs': 'Right backs',
    'lbs': 'Left backs',
    'cms': 'Central midfielders',
    'rms': 'Right wingers',
    'lms': 'Left wingers',
    'sts': 'Strikers',
}

POSITION_LINE_CHOICES = [
    ('GK', 'GK'),
    ('DEF', 'DEF'),
    ('MID', 'MID'),
    ('ATT', 'ATT'),
]

POSITION_LINE_MAP = {
    'GK': ['GK'],
    'DEF': ['RB', 'RWB', 'CB', 'LB', 'LWB'],
    'MID': ['CDM', 'CM', 'CAM', 'RM', 'RW', 'LM', 'LW'],
    'ATT': ['CF', 'ST', 'RF', 'LF']
}

POSITION_FILTER_MAP = {
    'DEF': POSITION_LINE_MAP['DEF'],
    'MID': POSITION_LINE_MAP['MID'],
    'ATT': POSITION_LINE_MAP['ATT'],
    'GK': ['GK'],
    'RWB': ['RWB'],
    'RB': ['RB'],
    'CB': ['CB'],
    'LB': ['LB'],
    'LWB': ['LWB'],
    'CDM': ['CDM'],
    'CM': ['CM'],
    'CAM': ['CAM'],
    'RM': ['RM'],
    'RW': ['RW'],
    'RF': ['RF'],
    'LM': ['LM'],
    'LW': ['LW'],
    'LF': ['LF'],
    'CF': ['CF'],
    'ST': ['ST'],
    'CBS': ['CB'],
    'RBS': ['RB', 'RWB'],
    'LBS': ['LB', 'LWB'],
    'CMS': ['CDM', 'CM', 'CAM'],
    'RMS': ['RM', 'RW', 'CF'],
    'LMS': ['LM', 'LW', 'LF'],
    'STS': ['CF', 'ST'],
}

POSITION_TO_AVAILABLE_POSITIONS = {
    'GK': ['GK'],
    'RB': ['RB', 'RWB'],
    'RWB': ['RB', 'RWB'],
    'LB': ['LB', 'LWB'],
    'LWB': ['LB', 'LWB'],
    'CB': ['CB'],
    'CDM': ['CDM', 'CM', 'CAM', 'CF', 'ST'],
    'CM': ['CDM', 'CM', 'CAM', 'CF', 'ST'],
    'CAM': ['CDM', 'CM', 'CAM', 'CF', 'ST'],
    'RM': ['RM', 'RW', 'RF'],
    'RW': ['RM', 'RW', 'RF'],
    'RF': ['RM', 'RW', 'RF'],
    'LM': ['LM', 'LW', 'LF'],
    'LW': ['LM', 'LW', 'LF'],
    'LF': ['LM', 'LW', 'LF'],
    'CF': ['CDM', 'CM', 'CAM', 'CF', 'ST'],
    'ST': ['CDM', 'CM', 'CAM', 'CF', 'ST'],
}

QUALITY_CHOICES = [
    ('bronze', 'bronze'),
    ('silver', 'silver'),
    ('gold', 'gold'),
]

QUALITY_TYPES = {
    'normal': ['bronze', 'silver', 'gold', 'rare_bronze', 'rare_silver', 'rare_gold'],
    'totw': ['totw_bronze', 'totw_silver', 'totw_gold'],
    'legend': ['legend'],
    'special': ['ones_to_watch', 'fut_champions_bronze', 'fut_champions_silver', 'fut_champions_gold',
                'sbc_base', 'halloween', 'movember', 'award_winner', 'confederation_champions_motm',
                'gotm', 'toty', 'imotm', 'st_patricks', 'fut_birthday', 'tots_bronze', 'tots_silver',
                'tots_gold', 'pink', 'futties_winner']
}

SORT_GET_TO_LABEL = {
    'likes': 'Likes',
    'rating': 'Rating',
    'acceleration': 'Acceleration',
    'sprint_speed': 'Sprint speed',
    'finishing': 'Finishing',
    'long_shots': 'Long shots',
    'penalties': 'Penalties',
    'positioning': 'Positioning',
    'shot_power': 'Shot power',
    'volleys': 'Volleys',
    'crossing': 'Crossing',
    'curve': 'Curve',
    'free_kick_accuracy': 'Free kick',
    'long_passing': 'Long passing',
    'short_passing': 'Short passing',
    'vision': 'Vision',
    'agility': 'Agility',
    'balance': 'Balance',
    'ball_control': 'Ball control',
    'dribbling': 'Dribbling',
    'reactions': 'Reactions',
    'heading': 'Heading',
    'interceptions': 'Interceptions',
    'marking': 'Marking',
    'sliding_tackle': 'Sliding tackle',
    'standing_tackle': 'Standing tackle',
    'aggression': 'Aggression',
    'jumping': 'Jumping',
    'stamina': 'Stamina',
    'strength': 'Strength',
    'rating_attacker': 'Attacker',
    'rating_creator': 'Creator',
    'rating_defender': 'Defender',
    'rating_creative': 'Pirlo',
    'rating_beast': 'Beast',
    'card_att_1': 'Pace',
    'card_att_2': 'Shooting',
    'card_att_3': 'Passing',
    'card_att_4': 'Dribbling',
    'card_att_5': 'Defending',
    'card_att_6': 'Physical',
    'total_stats': 'Total stats',
    'total_ingame_stats': 'Total ingame stats',
    'birth_date': 'Age',
}

SORT_CHOICES = [
    {'key': 'likes', 'label': 'Likes'},
    {'key': 'rating', 'label': 'Rating'},
    {
        'key': '', 'label': 'Pace', 'group': True, 'options': [
            {'key': 'acceleration', 'label': 'Acceleration'},
            {'key': 'sprint_speed', 'label': 'Sprint speed'},
        ]
    },
    {
        'key': '', 'label': 'Shooting', 'group': True, 'options': [
            {'key': 'finishing', 'label': 'Finishing'},
            {'key': 'long_shots', 'label': 'Long shots'},
            {'key': 'penalties', 'label': 'Penalties'},
            {'key': 'positioning', 'label': 'Positioning'},
            {'key': 'shot_power', 'label': 'Shot power'},
            {'key': 'volleys', 'label': 'Volleys'},
        ]
    },
    {
        'key': '', 'label': 'Passing', 'group': True, 'options': [
            {'key': 'crossing', 'label': 'Crossing'},
            {'key': 'curve', 'label': 'Curve'},
            {'key': 'free_kick_accuracy', 'label': 'Free kick'},
            {'key': 'long_passing', 'label': 'Long passing'},
            {'key': 'short_passing', 'label': 'Short passing'},
            {'key': 'vision', 'label': 'Vision'},
        ]
    },
    {
        'key': '', 'label': 'Dribbling', 'group': True, 'options': [
            {'key': 'agility', 'label': 'Agility'},
            {'key': 'balance', 'label': 'Balance'},
            {'key': 'ball_control', 'label': 'Ball control'},
            {'key': 'dribbling', 'label': 'Dribbling'},
            {'key': 'reactions', 'label': 'Reactions'},
        ]
    },
    {
        'key': '', 'label': 'Defending', 'group': True, 'options': [
            {'key': 'heading', 'label': 'Heading'},
            {'key': 'interceptions', 'label': 'Interceptions'},
            {'key': 'marking', 'label': 'Marking'},
            {'key': 'sliding_tackle', 'label': 'Sliding tackle'},
            {'key': 'standing_tackle', 'label': 'Standing tackle'},
        ]
    },
    {
        'key': '', 'label': 'Physical', 'group': True, 'options': [
            {'key': 'aggression', 'label': 'Aggression'},
            {'key': 'jumping', 'label': 'Jumping'},
            {'key': 'stamina', 'label': 'Stamina'},
            {'key': 'strength', 'label': 'Strength'},
        ]
    },
    {
        'key': '', 'label': 'Futily', 'group': True, 'options': [
            {'key': 'rating_attacker', 'label': 'Attacker'},
            {'key': 'rating_creator', 'label': 'Creator'},
            {'key': 'rating_defender', 'label': 'Defender'},
            {'key': 'rating_creative', 'label': 'Pirlo'},
            {'key': 'rating_beast', 'label': 'Beast'},
        ]
    },
    {'key': 'card_att_1', 'label': 'Pace'},
    {'key': 'card_att_2', 'label': 'Shooting'},
    {'key': 'card_att_3', 'label': 'Passing'},
    {'key': 'card_att_4', 'label': 'Dribbling'},
    {'key': 'card_att_5', 'label': 'Defending'},
    {'key': 'card_att_6', 'label': 'Physical'},
    {'key': 'total_stats', 'label': 'Total stats'},
    {'key': 'total_ingame_stats', 'label': 'Total ingame stats'},
    {'key': 'birth_date', 'label': 'Age'},
]

WORKRATE_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]
