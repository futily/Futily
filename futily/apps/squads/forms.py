from django import forms
from django.core.exceptions import ValidationError
from django.db.models import FileField

from ..players.models import Player
from .models import Squad


class BuilderFormBase(forms.Form):

    def clean_players(self):
        players = self.data.getlist('players', None)
        players = list(filter(None, players))

        if players:
            players = list(map(setup_squad_player, players))

            self.cleaned_data['players'] = players

        return players

    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    if name != 'players':
                        value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self.add_error(name, e)


class BuilderForm(BuilderFormBase, forms.ModelForm):

    class Meta:
        model = Squad
        fields = ['title', 'page', 'user', 'players', 'formation', 'chemistry', 'rating', 'attack', 'midfield',
                  'defence', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']


class SBCBuilderForm(BuilderFormBase, forms.ModelForm):

    class Meta:
        model = Squad
        fields = ['title', 'page', 'sbc', 'user', 'players', 'formation', 'chemistry', 'rating', 'loyalty',
                  'position_changes']


def setup_squad_player(player):
    split = player.split(',')

    return {
        'player': Player.objects.get(id=split[0]),
        'index': split[1],
        'position': split[2],
        'chemistry': split[3],
    }
