from django import forms

from ..players.models import Player
from .models import Squad


class BuilderForm(forms.ModelForm):
    class Meta:
        model = Squad
        exclude = ['players', 'slug']

    def clean(self):
        super(BuilderForm, self).clean()

        players = self.data.getlist('players', None)
        players = list(filter(None, players))

        if players:
            players = list(map(setup_squad_player, players))

            self.cleaned_data['players'] = players

        return self.cleaned_data


def setup_squad_player(player):
    split = player.split(',')

    return {
        'player': Player.objects.get(id=split[0]),
        'index': split[1],
        'position': split[2],
        'chemistry': split[3],
    }
