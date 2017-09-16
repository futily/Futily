from django import forms
from django.utils.text import slugify

from ..players.models import Player
from .models import Squad


class BuilderForm(forms.ModelForm):
    slug = forms.TextInput()

    class Meta:
        model = Squad
        exclude = ['players', 'slug']

    def clean(self):
        super(BuilderForm, self).clean()

        players = self.data.get('players', None)
        slug = self.data.get('slug', None)

        if players:
            player_splits = players.split('|')
            players = list(map(setup_squad_player, player_splits))

            self.cleaned_data['players'] = players

        self.cleaned_data['slug'] = slugify(slug)

        return self.cleaned_data


def setup_squad_player(player):
    split = player.split(',')

    return Player.objects.get(id=split[0]), split[1], split[2]
