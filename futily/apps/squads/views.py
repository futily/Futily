import json
import urllib
from collections import OrderedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.text import slugify
from django.views.generic import (DeleteView, DetailView, FormView, ListView,
                                  UpdateView)
from django.views.generic.base import ContextMixin, TemplateView, View

from futily.apps.actions.utils import create_action
from futily.apps.clubs.templatetags.clubs import get_clubs_page
from futily.apps.leagues.templatetags.leagues import get_leagues_page
from futily.apps.nations.templatetags.nations import get_nations_page
from futily.apps.players.constants import POSITION_TO_AVAILABLE_POSITIONS
from futily.apps.players.models import Player
from futily.apps.players.templatetags.players import get_players_page
from futily.apps.squads.constants import FORMATION_POSITIONS
from futily.apps.squads.templatetags.squads import get_squads_page
from futily.apps.users.models import User

from .forms import BuilderForm
from .models import FORMATION_CHOICES, Squad, SquadPlayer, Vote


class Found(Exception):
    pass


class BaseBuilder(ContextMixin):
    model = Squad
    form_class = BuilderForm

    def get_context_data(self, **kwargs):
        context = super(BaseBuilder, self).get_context_data(**kwargs)

        context['formations'] = dict(OrderedDict(FORMATION_CHOICES))

        return context


class Builder(BaseBuilder, TemplateView):
    template_name = 'squads/squad_builder.html'
    initial_formation = '442'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['initial_players'] = {}

        if self.request.GET.get('players', None):
            context['initial_players'] = self.initial_players_from_players()
        elif self.request.GET.get('nation', None):
            context['initial_players'] = self.initial_players_from_nation()
        elif self.request.GET.get('league', None):
            context['initial_players'] = self.initial_players_from_league()

        return context

    def initial_players_from_players(self):
        player_ids = self.request.GET.getlist('players', None)
        players = Player.objects.filter(id__in=player_ids)
        indexes_to_fill = [x for x in range(0, 11)]
        indexes_to_fill.reverse()
        initial_players = {}

        for player in players:
            try:
                player_position = player.position
                available_positions = POSITION_TO_AVAILABLE_POSITIONS[player_position]
                # The index where the player gets placed initially
                formation_positions = [
                    (index, x, x == player_position)
                    for (index, x) in FORMATION_POSITIONS[self.initial_formation]['positions'].items()
                    if x in available_positions
                ]
                formation_positions.reverse()
                wanted_positions = list(filter(lambda x: x[2] is True, formation_positions))
                other_positions = list(filter(lambda x: x[2] is False, formation_positions))

                for wanted_position in wanted_positions:
                    index = wanted_position[0]

                    if not initial_players.get(index, None):
                        initial_players[index] = player
                        indexes_to_fill.remove(index)

                        raise Found

                for other_position in other_positions:
                    index = other_position[0]

                    if not initial_players.get(index, None):
                        initial_players[index] = player
                        indexes_to_fill.remove(index)

                        raise Found

                initial_players[indexes_to_fill[0]] = player
            except Found:
                continue

        return initial_players

    def initial_players_from_nation(self):
        nation = self.request.GET.get('nation')
        initial_qs = Player.objects.filter(nation=nation).order_by('?')
        gk = initial_qs.filter(position='GK')[:1][0]
        rb = initial_qs.filter(position__in=['RB', 'RWB'])[:1][0]
        rcb = initial_qs.filter(position='CB')[:1][0]
        lcb = initial_qs.filter(position='CB').exclude(id=rcb.id)[:1][0]
        lb = initial_qs.filter(position__in=['LB', 'LWB'])[:1][0]
        rm = initial_qs.filter(position__in=['RM', 'RW', 'RF'])[:1][0]
        rcm = initial_qs.filter(position__in=['CDM', 'CM', 'CAM'])[:1][0]
        lcm = initial_qs.filter(position__in=['CDM', 'CM', 'CAM']).exclude(id=rcm.id)[:1][0]
        lm = initial_qs.filter(position__in=['LM', 'LW', 'LF'])[:1][0]
        rs = initial_qs.filter(position__in=['CF', 'ST'])[:1][0]
        ls = initial_qs.filter(position__in=['CF', 'ST']).exclude(id=rs.id)[:1][0]

        return {
            0: gk,
            1: rb,
            2: rcb,
            3: lcb,
            4: lb,
            5: rm,
            6: rcm,
            7: lcm,
            8: lm,
            9: rs,
            10: ls
        }

    def initial_players_from_league(self):
        league = self.request.GET.get('league')
        initial_qs = Player.objects.filter(league=league).order_by('?')
        gk = initial_qs.filter(position='GK')[:1][0]
        rb = initial_qs.filter(position__in=['RB', 'RWB'])[:1][0]
        rcb = initial_qs.filter(position='CB')[:1][0]
        lcb = initial_qs.filter(position='CB').exclude(id=rcb.id)[:1][0]
        lb = initial_qs.filter(position__in=['LB', 'LWB'])[:1][0]
        rm = initial_qs.filter(position__in=['RM', 'RW', 'RF'])[:1][0]
        rcm = initial_qs.filter(position__in=['CDM', 'CM', 'CAM'])[:1][0]
        lcm = initial_qs.filter(position__in=['CDM', 'CM', 'CAM']).exclude(id=rcm.id)[:1][0]
        lm = initial_qs.filter(position__in=['LM', 'LW', 'LF'])[:1][0]
        rs = initial_qs.filter(position__in=['CF', 'ST'])[:1][0]
        ls = initial_qs.filter(position__in=['CF', 'ST']).exclude(id=rs.id)[:1][0]

        return {
            0: gk,
            1: rb,
            2: rcb,
            3: lcb,
            4: lb,
            5: rm,
            6: rcm,
            7: lcm,
            8: lm,
            9: rs,
            10: ls
        }


class BuilderAjax(FormView):
    def post(self, request, *args, **kwargs):
        form = BuilderForm(self.request.POST)

        # Create a json response object
        response_data = {
            'errors': {}
        }

        # If the form is invalid, fill response with errors
        if not form.is_valid():
            # Add error to response
            for key, value in form.errors.items():
                response_data['errors'][key] = json.loads(value.as_json())

            return JsonResponse(response_data, status=400)
        else:
            data = form.cleaned_data
            data['is_online'] = True
            data['robots_index'] = True
            data['robots_follow'] = True
            data['robots_archive'] = True

            players = data.pop('players')

            squad = Squad(**data)
            squad.user = request.user if request.user.is_authenticated else None
            squad.save()

            # Delete players that already exist on the squad
            SquadPlayer.objects.filter(squad=squad).delete()

            if players:
                for player in players:
                    p = SquadPlayer(player=player['player'], squad=squad, index=player['index'],
                                    position=player['position'], chemistry=player['chemistry'])
                    p.save()

            if request.user.is_authenticated:
                create_action(request.user, 'created squad', squad)

        return JsonResponse(response_data, status=200)


class BuilderImport(View):
    def get(self, request, *args, **kwargs):
        web_app_id = self.kwargs['id']
        url = f'https://utas.external.s3.fut.ea.com/ut/showofflink/{web_app_id}'
        json_data = json.loads(urllib.request.urlopen(url).read())
        squad_data = json_data['data']['squad'][0]
        formation = self.formation_schema(squad_data['formation'])
        players = [
            Player.objects.get(
                ea_id_base=x['itemData']['resourceId']
            ) for x in squad_data['players'] if x['itemData']['resourceId']]
        players = {
            x['index']: {
                'object': Player.objects.get(ea_id_base=x['itemData']['resourceId']),
                'position': x['itemData']['preferredPosition']
            } if x['itemData']['resourceId'] else None for x in squad_data['players']
        }
        title = json_data['squadname']
        web_app_url = json_data['url']

        response_data = {
            'squad': {
                'title': title,
                'slug': slugify(title),
                'formation': formation,
                'web_app_import': True,
                'web_app_url': web_app_url,
            },
            'players': [
                {
                    'index': index,
                    'player': {
                        'id': obj['object'].id,
                        'name': obj['object'].name,
                        'rating': obj['object'].rating,
                        'ea_id_base': obj['object'].ea_id_base
                    },
                    'position': obj['position']
                } for index, obj in players.items() if obj
            ]
        }

        return JsonResponse(response_data)

    @staticmethod
    def formation_schema(formation):
        return {
            'f3412': '3412',
            'f3421': '3421',
            'f343': '343',
            'f352': '352',
            'f41212': '41212',
            'f41212a': '41212-2',
            'f4141': '4141',
            'f4222': '4222',
            'f4231': '4231',
            'f4231a': '4231-2',
            'f4312': '4312',
            'f4321': '4321',
            'f433': '433',
            'f433a': '433-2',
            'f433b': '433-3',
            'f433c': '433-4',
            'f433d': '433-5',
            'f4411': '4411',
            'f442': '442',
            'f442a': '442-2',
            'f451': '451',
            'f451a': '451-2',
            'f5212': '5212',
            'f5221': '5221',
            'f532': '532',
        }[formation]


class SquadList(ListView):
    model = Squad
    paginate_by = 50

    def get_queryset(self):
        return super(SquadList, self).get_queryset().filter(page__page=self.request.pages.current)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['aside_links'] = [
            {
                'title': 'Players',
                'url': get_players_page().get_absolute_url(),
                'here': str(self.request.path == get_players_page().get_absolute_url()).lower(),
            },
            {
                'title': 'Clubs',
                'url': get_clubs_page().get_absolute_url(),
                'here': str(self.request.path == get_clubs_page().get_absolute_url()).lower(),
            },
            {
                'title': 'Leagues',
                'url': get_leagues_page().get_absolute_url(),
                'here': str(self.request.path == get_leagues_page().get_absolute_url()).lower(),
            },
            {
                'title': 'Nations',
                'url': get_nations_page().get_absolute_url(),
                'here': str(self.request.path == get_nations_page().get_absolute_url()).lower(),
            },
        ]

        return context


class TotwList(ListView):
    model = Squad
    paginate_by = 10
    template_name = 'squads/totw_list.html'

    def get_queryset(self):
        return super(TotwList, self).get_queryset().filter(page__page=self.request.pages.current, is_special=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['aside_links'] = [
            {
                'title': 'Players',
                'url': get_players_page().get_absolute_url(),
                'here': str(self.request.path == get_players_page().get_absolute_url()).lower(),
            },
            {
                'title': 'Clubs',
                'url': get_clubs_page().get_absolute_url(),
                'here': str(self.request.path == get_clubs_page().get_absolute_url()).lower(),
            },
            {
                'title': 'Leagues',
                'url': get_leagues_page().get_absolute_url(),
                'here': str(self.request.path == get_leagues_page().get_absolute_url()).lower(),
            },
            {
                'title': 'Nations',
                'url': get_nations_page().get_absolute_url(),
                'here': str(self.request.path == get_nations_page().get_absolute_url()).lower(),
            },
        ]

        return context


class SquadDetail(BaseBuilder, DetailView):
    model = Squad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['FORMATION_POSITIONS'] = FORMATION_POSITIONS[self.object.formation]

        return context


class SquadRate(LoginRequiredMixin, View):
    model = Vote

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())

        squad = Squad.objects.get(pk=data.get('object'))
        user = User.objects.get(pk=data.get('user'))
        action = data.get('action')

        try:
            if action == 'up':
                self.model.votes.up(squad, user)

                create_action(request.user, 'liked squad', squad)
            else:
                self.model.votes.down(squad, user)

                create_action(request.user, 'disliked squad', squad)

            if request.is_ajax():
                return JsonResponse(squad.squadrating.to_dict())

            return HttpResponseRedirect('/')
        except ValidationError as err:
            if request.is_ajax():
                return JsonResponse(data={'error': err.message}, status=400)

            return HttpResponseRedirect('/')


class SquadCopy(BaseBuilder, DeleteView):
    model = Squad

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.pk = None
        obj.user = request.user
        obj.save()

        for player in obj.players.all():
            player.pk = None
            player.squad = obj
            player.save()

        return HttpResponseRedirect(obj.get_update_url())


class SquadUpdate(BaseBuilder, UpdateView):
    model = Squad
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['FORMATION_POSITIONS'] = FORMATION_POSITIONS[self.object.formation]

        return context

    def get_form_kwargs(self):
        kwargs = super(SquadUpdate, self).get_form_kwargs()
        kwargs.update({'instance': self.object})

        return kwargs

    def form_valid(self, form):
        request = self.request
        data = form.cleaned_data

        players = data.pop('players')

        squad = form.save()

        # Delete players that already exist on the squad
        SquadPlayer.objects.filter(squad=squad).delete()

        if players:
            for player in players:
                try:
                    squad_player = SquadPlayer.objects.get(index=player['index'], squad=squad)
                except SquadPlayer.DoesNotExist:
                    squad_player = SquadPlayer(index=player['index'], squad=squad)

                squad_player.player = player['player']
                squad_player.position = player['position']
                squad_player.chemistry = player['chemistry']
                squad_player.save()

        if request.user.is_authenticated:
            create_action(request.user, 'updated squad', squad)

        return HttpResponseRedirect(self.get_success_url())
