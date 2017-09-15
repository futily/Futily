import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.text import slugify
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from rest_framework import filters, viewsets

from futily.apps.players.constants import (LEVEL_FILTER_MAP,
                                           LEVELS_GET_TO_LABEL,
                                           POSITION_FILTER_MAP,
                                           POSITION_GET_TO_LABEL)
from futily.apps.players.serializers import PlayerSerializer
from futily.apps.users.models import FavouritePlayers, User
from futily.apps.views import EaObjectDetail

from .forms import PlayerListForm
from .models import Player, Vote


class PlayerList(FormMixin, ListView):
    form_class = PlayerListForm
    model = Player
    paginate_by = 30
    success_url = '/'

    def get_initial(self):
        initial = super(PlayerList, self).get_initial()

        initial.update(self.request.GET)

        return initial

    def get_queryset(self):  # pylint: disable=too-complex, too-many-locals
        qs = super(PlayerList, self).get_queryset()

        current_filters = self.request.GET
        allowed_filters = self.allowed_filters()

        # Check if we have any filterable parameters
        if current_filters and set(current_filters.dict().keys()).issubset(set(allowed_filters)):
            if current_filters.get('min_rating') and current_filters.get('max_rating'):
                qs = qs.filter(rating__range=(current_filters.get('min_rating'), current_filters.get('max_rating')))

            if current_filters.get('position'):
                # If the value of this == 'all' then check the form submission in JS and clear this value if need be
                # Alternatively remove the 'all' option and just rely on the "clear" to remove it
                current_positions = current_filters.getlist('position')
                individual_positions = Player.objects.order_by('position').values_list('position', flat=True).distinct()
                line_positions = Player.objects.order_by('position_line').values_list('position_line', flat=True).distinct()
                position_schema = {x.lower(): {'position__in': [x.upper()]} for x in individual_positions}
                position_schema.update({x.lower(): {'position_line__in': [x.upper()]} for x in line_positions})
                position_schema.update({
                    'cbs': {'position__in': ['CB']},
                    'rbs': {'position__in': ['RB', 'RWB']},
                    'lbs': {'position__in': ['LB', 'LWB']},
                    'cms': {'position__in': ['CDM', 'CM', 'CAM']},
                    'rms': {'position__in': ['RM', 'RW', 'RF']},
                    'lms': {'position__in': ['LM', 'LW', 'LF']},
                    'sts': {'position__in': ['CF', 'ST']},
                })

                position_filter = construct_query_dict(current_positions, position_schema)
                queries = [Q(**{key: value}) for key, value in position_filter.items()]
                query = queries.pop()

                for item in queries:
                    query |= item

                qs = qs.filter(query)

            if current_filters.get('level'):
                current_levels = current_filters.getlist('level')
                available_levels = Player.objects.order_by('color').values_list('color', flat=True).distinct()
                gold_levels = [x for x in available_levels if 'gold' in x]
                silver_levels = [x for x in available_levels if 'silver' in x]
                bronze_levels = [x for x in available_levels if 'bronze' in x]
                special_levels = [x for x in available_levels if x not in gold_levels + silver_levels + bronze_levels]
                level_schema = {
                    'legend': {'color__in': [x for x in available_levels if 'legend' in x]},
                    'special': {'color__in': special_levels},
                    'gold': {'color__in': gold_levels},
                    'silver': {'color__in': silver_levels},
                    'bronze': {'color__in': bronze_levels},
                    'totw_all': {'color__in': [
                        x for x in bronze_levels + silver_levels + gold_levels if 'totw' in x]},
                    'totw_gold': {'color__in': [x for x in gold_levels if 'totw' in x]},
                    'totw_silver': {'color__in': [x for x in silver_levels if 'totw' in x]},
                    'totw_bronze': {'color__in': [x for x in bronze_levels if 'totw' in x]},
                    'gold_rare': {'color__in': [x for x in gold_levels if 'rare' in x]},
                    'gold_common': {'color__in': ['gold']},
                    'silver_rare': {'color__in': [x for x in silver_levels if 'rare' in x]},
                    'silver_common': {'color__in': ['silver']},
                    'bronze_rare': {'color__in': [x for x in bronze_levels if 'rare' in x]},
                    'bronze_common': {'color__in': ['bronze']},
                    'award_winner': {'color__in': ['award_winner']},
                    'confederation_champions_motm': {'color__in': ['confederation_champions_motm']},
                    'fut_birthday': {'color__in': ['fut_birthday']},
                    'gotm': {'color__in': ['gotm']},
                    'halloween': {'color__in': ['halloween']},
                    'imotm': {'color__in': ['imotm']},
                    'motm': {'color__in': ['motm']},
                    'movember': {'color__in': ['movember']},
                    'ones_to_watch': {'color__in': ['ones_to_watch']},
                    'purple': {'color__in': ['purple']},
                    'record_breaker': {'color__in': ['record_breaker']},
                    'sbc_base': {'color__in': ['sbc_base']},
                    'st_patricks': {'color__in': ['st_patricks']},
                    'tots': {'color__in': ['tots']},
                    'toty': {'color__in': ['toty']},
                }

                color_filter = construct_query_dict(current_levels, level_schema)

                qs = qs.filter(**color_filter)

            if current_filters.get('nation'):
                qs = qs.filter(nation__slug__in=current_filters.getlist('nation'))

            if current_filters.get('league'):
                qs = qs.filter(league__slug__in=current_filters.getlist('league'))

            if current_filters.get('skills'):
                qs = qs.filter(skill_moves=current_filters.get('skills'))

            if current_filters.get('weak_foot'):
                qs = qs.filter(weak_foot=current_filters.get('weak_foot'))

            if current_filters.get('def_workrate'):
                qs = qs.filter(work_rate_def=current_filters.get('def_workrate').title())

            if current_filters.get('att_workrate'):
                qs = qs.filter(work_rate_att=current_filters.get('att_workrate').title())

            if current_filters.get('strong_foot'):
                qs = qs.filter(foot=current_filters.get('strong_foot').title())

        return qs

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        return super(PlayerList, self).get_context_data(**kwargs)

    def allowed_filters(self):
        form = self.get_form()

        return [x.html_name for x in form]


class PlayerListNew(ListView):
    model = Player
    paginate_by = 30
    ordering = '-created'
    template_name = 'players/player_list_new.html'

    def is_filtered(self):
        return self.request.GET.get('position') or self.request.GET.get('level')

    def is_sorted(self):
        return self.request.GET.get('sort')

    def get_context_data(self, **kwargs):
        context = super(PlayerListNew, self).get_context_data()

        context['players'] = self.player_pagination(self.get_queryset())

        current_position = self.request.GET.get('position')
        current_level = self.request.GET.get('level')
        context['filters'] = {
            'positions': {
                'choices': self.filters['positions'],
                'current': current_position,
                'label': POSITION_GET_TO_LABEL[current_position] if current_position else 'All',
            },
            'levels': {
                'choices': self.filters['levels'],
                'current': current_level,
                'label': LEVELS_GET_TO_LABEL[current_level] if current_level else 'All',
            }
        }

        return context

    def get_players_queryset(self, players):
        if self.is_filtered():
            position = self.request.GET.get('position')
            level = self.request.GET.get('level')

            if position:
                players = players.filter(
                    position__in=POSITION_FILTER_MAP[position.upper()]
                )

            if level:
                players = players.filter(
                    color__in=LEVEL_FILTER_MAP[level.upper()]
                )

        return players

    def player_pagination(self, players):
        paginator = Paginator(self.get_players_queryset(players), self.paginate_by)

        try:
            # Deliver the requested page
            return paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            return paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return paginator.page(paginator.num_pages)

    @property
    def filters(self):
        return {
            'levels': [
                {'key': 'all', 'label': 'All', 'group': False},
                {'key': 'totw', 'label': 'TOTW', 'group': False},
                {'key': 'gold', 'label': 'Gold', 'group': False},
                {'key': 'silver', 'label': 'Silver', 'group': False},
                {'key': 'bronze', 'label': 'Bronze', 'group': False},
                {'key': '', 'label': 'TOTW', 'group': True, 'options': [
                    {'key': 'totw-gold', 'label': 'TOTW Gold'},
                    {'key': 'totw-silver', 'label': 'TOTW Silver'},
                    {'key': 'totw-bronze', 'label': 'TOTW Bronze'},
                ]},
                {'key': '', 'label': 'Rares', 'group': True, 'options': [
                    {'key': 'rare-gold', 'label': 'Rare Gold'},
                    {'key': 'rare-silver', 'label': 'Rare Silver'},
                    {'key': 'rare-bronze', 'label': 'Rare Bronze'},
                ]},
                {'key': '', 'label': 'Non rares', 'group': True, 'options': [
                    {'key': 'nonrare-gold', 'label': 'Gold'},
                    {'key': 'nonrare-silver', 'label': 'Silver'},
                    {'key': 'nonrare-bronze', 'label': 'Bronze'},
                ]},
                {'key': 'legend', 'label': 'Legends'},
                {'key': 'toty', 'label': 'TOTY'},
                {'key': 'motm', 'label': 'MOTM'},
                {'key': 'transfers', 'label': 'Transfers'},
                {'key': 'special', 'label': 'Special'},
            ],
            'positions': [
                {'key': 'all', 'label': 'All positions'},
                {'key': 'gk', 'label': 'Goalkeepers'},
                {'key': 'def', 'label': 'Defenders'},
                {'key': 'mid', 'label': 'Midfielders'},
                {'key': 'att', 'label': 'Attackers'},
                {'key': '', 'label': 'Positions', 'group': True, 'options': [
                    {'key': 'gk', 'label': 'GK'},
                    {'key': 'rwb', 'label': 'RWB'},
                    {'key': 'rb', 'label': 'RB'},
                    {'key': 'cb', 'label': 'CB'},
                    {'key': 'lb', 'label': 'LB'},
                    {'key': 'lwb', 'label': 'LWB'},
                    {'key': 'cdm', 'label': 'CDM'},
                    {'key': 'cm', 'label': 'CM'},
                    {'key': 'cam', 'label': 'CAM'},
                    {'key': 'rm', 'label': 'RM'},
                    {'key': 'rw', 'label': 'RW'},
                    {'key': 'rf', 'label': 'RF'},
                    {'key': 'lm', 'label': 'LM'},
                    {'key': 'lw', 'label': 'LW'},
                    {'key': 'lf', 'label': 'LF'},
                    {'key': 'cf', 'label': 'CF'},
                    {'key': 'st', 'label': 'ST'},
                ]},
                {'key': 'gk', 'label': 'Goalkeepers'},
                {'key': 'cbs', 'label': 'Center backs'},
                {'key': 'rbs', 'label': 'Right backs'},
                {'key': 'lbs', 'label': 'Left backs'},
                {'key': 'cms', 'label': 'Central midfielders'},
                {'key': 'rms', 'label': 'Right wingers'},
                {'key': 'lms', 'label': 'Left wingers'},
                {'key': 'sts', 'label': 'Strikers'},
            ]
        }


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

        player = Player.objects.get(pk=data.get('player'))
        user = User.objects.get(pk=data.get('user'))
        action = data.get('action')

        try:
            if action == 'up':
                self.model.votes.up(player, user)
            else:
                self.model.votes.down(player, user)

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
        else:
            user.favouriteplayers.players.add(player)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class PlayerDetailChemistry(DetailView):
    model = Player
    template_name = 'players/player_detail_chemistry.html'


class PlayerDetailChemistryType(EaObjectDetail):
    model = Player
    template_name = 'players/player_detail_chemistry_type.html'

    def initial_players(self):
        return self.object.get_chemistry_players()[self.kwargs['chem_type']]


class PlayerDetailSimilar(EaObjectDetail):
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


class PlayerViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_fields = ['first_name', 'last_name', 'common_name']

    def get_queryset(self):
        query = self.request.query_params.get('query')
        ids = None

        if self.request.query_params.get('ids'):
            ids = self.request.query_params.get('ids').split(',')[:-1]

        qs = Player.objects.all()

        if ids:
            qs = qs.filter(ea_id_base__in=ids)

        if query:
            qs = qs.filter(english_names__icontains=query)

        nation = self.request.query_params.get('nation')

        if nation:
            qs = qs.filter(nation__slug=slugify(nation))

        return qs
