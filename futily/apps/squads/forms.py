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

    return Player.objects.get(id=split[0]), split[1], split[2]
