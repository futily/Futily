from django import forms

from futily.apps.leagues.models import League
from futily.apps.players.constants import SPECIAL_COLOR_CHOICES
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
        ('TOTW', [
            ('totw_all', 'All TOTW'),
            ('totw_gold', 'TOTW Gold'),
            ('totw_silver', 'TOTW Silver'),
            ('totw_bronze', 'TOTW Bronze'),
        ]),
        ('Non In-Forms', [
            ('nif_all', 'All Non-IF'),
            ('nif_gold', 'Non-IF Gold'),
            ('nif_silver', 'Non-IF Silver'),
            ('nif_bronze', 'Non-IF Bronze'),
        ]),
        ('Rares', [
            ('rare_all', 'All Rare'),
            ('rare_gold', 'Rare Gold'),
            ('rare_silver', 'Rare Silver'),
            ('rare_bronze', 'Rare Bronze'),
        ]),
        ('Non Rares', [
            ('common_all', 'All'),
            ('common_gold', 'Gold'),
            ('common_silver', 'Silver'),
            ('common_bronze', 'Bronze'),
        ]),
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

        color_choices = Player.objects.only('color').values_list('color', flat=True).order_by('color').distinct('color')
        self.fields['level'].choices += [
            ('Individuals', [
                (value, label) for (value, label) in SPECIAL_COLOR_CHOICES
                if value in color_choices and 'totw' not in value
            ])
        ]

        self.fields['nation'].choices = [
            ('Top Nations', [
                x for x in Nation.objects.order_by('-total_gold')[:10]
            ]),
            ('All Nations', [
                x for x in Nation.objects.order_by('title') if x.has_players
            ]),
        ]

        self.fields['league'].choices = [
            ('Top Leagues', [
                x for x in League.objects.order_by('-total_gold')[:5]
            ]),
            ('All Leagues', [
                x for x in League.objects.order_by('title') if x.has_players
            ]),
        ]
