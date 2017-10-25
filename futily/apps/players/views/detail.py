import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import DetailView

from futily.apps.actions.utils import create_action
from futily.apps.players.models import Player, Vote
from futily.apps.users.models import FavouritePlayers, User
from futily.apps.views import PlayerFilterSorted


class PlayerDetail(DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['chemistry_styles'] = [
            {'label': 'basic', 'items': [
                (1, 'PAC'), (1, 'SHO'), (1, 'PAS'), (1, 'DRI'), (1, 'DEF'), (1, 'PHY')],
             'type': 'basic'},
            {'label': 'sniper', 'items': [(3, 'SHO'), (3, 'DRI')], 'type': 'att'},
            {'label': 'finisher', 'items': [(3, 'SHO'), (3, 'PHY')], 'type': 'att'},
            {'label': 'deadeye', 'items': [(3, 'SHO'), (3, 'PAS')], 'type': 'att'},
            {'label': 'marksman', 'items': [(2, 'SHO'), (2, 'DRI'), (2, 'PHY')], 'type': 'att'},
            {'label': 'hawk', 'items': [(2, 'PAC'), (2, 'SHO'), (2, 'PHY')], 'type': 'att'},
            {'label': 'artist', 'items': [(3, 'PAS'), (3, 'DRI')], 'type': 'mid'},
            {'label': 'architect', 'items': [(3, 'PAS'), (3, 'PHY')], 'type': 'mid'},
            {'label': 'powerhouse', 'items': [(3, 'PAS'), (3, 'DEF')], 'type': 'mid'},
            {'label': 'maestro', 'items': [(2, 'SHO'), (2, 'PAS'), (2, 'DRI')], 'type': 'mid'},
            {'label': 'engine', 'items': [(2, 'PAC'), (2, 'PAS'), (2, 'DRI')], 'type': 'mid'},
            {'label': 'sentinel', 'items': [(3, 'DEF'), (3, 'PHY')], 'type': 'def'},
            {'label': 'guardian', 'items': [(3, 'DRI'), (3, 'DEF')], 'type': 'def'},
            {'label': 'gladiator', 'items': [(3, 'SHO'), (3, 'DEF')], 'type': 'def'},
            {'label': 'backbone', 'items': [(2, 'PAS'), (2, 'DEF'), (2, 'PHY')], 'type': 'def'},
            {'label': 'anchor', 'items': [(2, 'PAC'), (2, 'DEF'), (2, 'PHY')], 'type': 'def'},
            {'label': 'hunter', 'items': [(3, 'PAC'), (3, 'SHO')], 'type': 'skill'},
            {'label': 'catalyst', 'items': [(3, 'PAC'), (3, 'PAS')], 'type': 'skill'},
            {'label': 'shadow', 'items': [(3, 'PAC'), (3, 'DEF')], 'type': 'skill'},
        ]

        return context


class PlayerRate(LoginRequiredMixin, View):
    model = Vote

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())

        player = Player.objects.get(pk=data.get('object'))
        user = User.objects.get(pk=data.get('user'))
        action = data.get('action')

        try:
            if action == 'up':
                self.model.votes.up(player, user)

                create_action(request.user, 'liked player', player)
            else:
                self.model.votes.down(player, user)

                create_action(request.user, 'disliked player', player)

            if request.is_ajax():
                return JsonResponse(player.playerrating.to_dict())

            return HttpResponseRedirect('/')
        except ValidationError as err:
            if request.is_ajax():
                return JsonResponse(data={'error': err.message}, status=400)

            return HttpResponseRedirect('/')


class PlayerFavourite(LoginRequiredMixin, View):
    model = FavouritePlayers

    def get(self, request, *args, **kwargs):
        user = self.request.user
        player = Player.objects.get(pk=self.kwargs.get('pk'))

        if player in user.favouriteplayers.players.all():
            user.favouriteplayers.players.remove(player)

            create_action(request.user, 'unfavourited', player)
        else:
            user.favouriteplayers.players.add(player)

            create_action(request.user, 'favourited', player)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class PlayerDetailChemistry(DetailView):
    model = Player
    template_name = 'players/player_detail_chemistry.html'


class PlayerDetailChemistryType(DetailView, PlayerFilterSorted):
    model = Player
    template_name = 'players/player_detail_chemistry_type.html'

    def initial_players(self):
        return self.object.get_chemistry_players()[self.kwargs['chem_type']]


class PlayerDetailSimilar(DetailView, PlayerFilterSorted):
    model = Player
    template_name = 'players/player_detail_similar.html'

    def initial_players(self):
        if self.is_sorted():
            return self.object.get_similar_players(sort=self.is_sorted())

        return self.object.get_similar_players()


class PlayerDetailCompare(DetailView):
    model = Player
    template_name = 'players/player_detail_compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get('other_pk'):
            context['other_player'] = Player.objects.get(pk=self.kwargs.get('other_pk'))
        else:
            context['other_player'] = Player.objects.last()

        return context


def construct_query_dict(current, schema):
    filter_dict = {}
    wanted = []

    for position in current:
        wanted.append(schema[position])

    for color in wanted:
        for key, value in color.items():
            if key not in filter_dict:
                filter_dict[key] = value
            elif key in filter_dict:
                filter_dict[key] += value
                filter_dict[key] = list(set(filter_dict[key]))

    return filter_dict
