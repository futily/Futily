from django import forms

from futily.apps.leagues.models import League
from futily.apps.players.models import Player

from ..nations.models import Nation

WORKRATE_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


class PlayerListForm(forms.Form):
    # Initial and min_value is done in the __init__
    min_rating = forms.IntegerField(max_value=99)
    max_rating = forms.IntegerField(max_value=99)
    position = forms.MultipleChoiceField(choices=[
        ('Lines', [
            ('all', 'All positions'),
            ('gk', 'Goalkeepers'),
            ('def', 'Defenders'),
            ('mid', 'Midfielders'),
            ('att', 'Attackers'),
        ]),
        ('Individuals', [
            ('gk', 'GK'),
            ('rwb', 'RWB'),
            ('rb', 'RB'),
            ('cb', 'CB'),
            ('lb', 'LB'),
            ('lwb', 'LWB'),
            ('cdm', 'CDM'),
            ('cm', 'CM'),
            ('cam', 'CAM'),
            ('rm', 'RM'),
            ('rw', 'RW'),
            ('rf', 'RF'),
            ('lm', 'LM'),
            ('lw', 'LW'),
            ('lf', 'LF'),
            ('cf', 'CF'),
            ('st', 'ST'),
        ]),
        ('Groups', [
            ('gk', 'Goalkeepers'),
            ('cbs', 'Center backs'),
            ('rbs', 'Right backs'),
            ('lbs', 'Left backs'),
            ('cms', 'Central midfielders'),
            ('rms', 'Right wingers'),
            ('lms', 'Left wingers'),
            ('sts', 'Strikers'),
        ]),
    ])
    level = forms.MultipleChoiceField(choices=[
        ('Base', [
            ('legend', 'Legends'),
            ('special', 'Specials'),
            ('gold', 'Gold'),
            ('silver', 'Silver'),
            ('bronze', 'Bronze'),
        ]),
        ('In-Forms', [
            ('if-all', 'All IF'),
            ('if-gold', 'IF Gold'),
            ('if-silver', 'IF Silver'),
            ('if-bronze', 'IF Bronze'),
        ]),
        ('Non In-Forms', [
            ('nif-all', 'All Non-IF'),
            ('nif-gold', 'Non-IF Gold'),
            ('nif-silver', 'Non-IF Silver'),
            ('nif-bronze', 'Non-IF Bronze'),
        ]),
        ('Rares', [
            ('rare-all', 'All Rare'),
            ('rare-gold', 'Rare Gold'),
            ('rare-silver', 'Rare Silver'),
            ('rare-bronze', 'Rare Bronze'),
        ]),
        ('Non Rares', [
            ('nonrare-all', 'All'),
            ('nonrare-gold', 'Gold'),
            ('nonrare-silver', 'Silver'),
            ('nonrare-bronze', 'Bronze'),
        ]),
        ('Individuals', [
            ('award_winner', 'Award Winner'),
            ('confederation_champions_motm', 'Confederation Champions MOTM'),
            ('fut_birthday', 'FUT Birthday'),
            ('gotm', 'gotm'),
            ('halloween', 'Halloween'),
            ('imotm', 'iMOTM'),
            ('motm', 'MOTM'),
            ('movember', 'Movember'),
            ('ones_to_watch', 'Ones to watch'),
            ('purple', 'Purple'),
            ('record_breaker', 'Record Breaker'),
            ('sbc_base', 'SBC'),
            ('st_patricks', 'St Patricks'),
            ('tots', 'TOTS'),
            ('toty', 'TOTY'),
        ])
    ])

    # Choices are done in the __init__
    nation = forms.MultipleChoiceField()
    league = forms.MultipleChoiceField()
    skills = forms.ChoiceField(choices=[(str(x), str(x)) for x in range(1, 6)])
    weak_foot = forms.ChoiceField(choices=[(str(x), str(x)) for x in range(1, 6)])
    def_workrate = forms.ChoiceField(choices=WORKRATE_CHOICES, widget=forms.RadioSelect)
    att_workrate = forms.ChoiceField(choices=WORKRATE_CHOICES, widget=forms.RadioSelect)
    strong_foot = forms.ChoiceField(choices=[('right', 'Right'), ('left', 'Left')], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(PlayerListForm, self).__init__(*args, **kwargs)

        lowest_player_rating = Player.objects.order_by('rating').first().rating

        self.fields['min_rating'].min_value = lowest_player_rating
        self.fields['min_rating'].initial = lowest_player_rating
        self.fields['max_rating'].min_value = lowest_player_rating
        self.fields['max_rating'].initial = 99

        self.fields['nation'].choices = [
            ('Top Nations', [
                (x.slug, x.title) for x in Nation.objects.order_by('-total_players')[:10]
            ]),
            ('All Nations', [
                (x.slug, x.title) for x in Nation.objects.order_by('title')
            ]),
        ]

        self.fields['league'].choices = [
            ('Top Leagues', [
                (x.slug, x.title) for x in League.objects.order_by('-total_players')[:5]
            ]),
            ('All Leagues', [
                (x.slug, x.title) for x in League.objects.order_by('title')
            ]),
        ]
