COLOR_CHOICES = [
    ('bronze', 'Bronze'),
    ('silver', 'Silver'),
    ('gold', 'Gold'),
    ('rare_bronze', 'Rare bronze'),
    ('rare_silver', 'Rare silver'),
    ('rare_gold', 'Rare gold'),
    ('totw_bronze', 'TOTW bronze'),
    ('totw_silver', 'TOTW silver'),
    ('totw_gold', 'TOTW gold'),
    ('legend', 'Legend'),
    ('ones_to_watch', 'Ones to watch'),
    ('fut_champions_bronze', 'FUT champions bronze'),
    ('fut_champions_silver', 'FUT champions silver'),
    ('fut_champions_gold', 'FUT champions gold'),
    ('sbc_base', 'SBC base'),
    ('halloween', 'Halloween'),
    ('movember', 'Movember'),
    ('award_winner', 'Award winner'),
    ('confederation_champions_motm', 'Confederation champions MOTM'),
    ('gotm', 'GOTM'),
    ('toty', 'TOTY'),
    ('imotm', 'iMOTM'),
    ('st_patricks', 'St. Patricks'),
    ('fut_birthday', 'FUT birthday'),
    ('tots_bronze', 'TOTS bronze'),
    ('tots_silver', 'TOTS silver'),
    ('tots_gold', 'TOTS gold'),
    ('pink', 'Pink'),
    ('futties_winner', 'Futties winner'),
]

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

QUALITY_CHOICES = [
    ('bronze', 'bronze'),
    ('silver', 'silver'),
    ('gold', 'gold'),
]

WORKRATE_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]
