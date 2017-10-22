from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import ContextMixin

from futily.apps.clubs.templatetags.clubs import get_clubs_page
from futily.apps.leagues.templatetags.leagues import get_leagues_page
from futily.apps.nations.templatetags.nations import get_nations_page
from futily.apps.players.constants import (LEVEL_FILTER_MAP,
                                           LEVELS_GET_TO_LABEL,
                                           POSITION_FILTER_MAP,
                                           POSITION_GET_TO_LABEL,
                                           SORT_GET_TO_LABEL)
from futily.apps.players.templatetags.players import get_players_page


class PlayerFilterSorted(ContextMixin, View):
    always_filters = None
    players_per_page = 30

    def is_filtered(self):
        return self.request.GET.get('position') or self.request.GET.get('level')

    def is_sorted(self):
        return self.request.GET.get('sort')

    def initial_players(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['players'] = self.player_pagination(self.initial_players())

        current_position = self.request.GET.get('position')
        current_level = self.request.GET.get('level')
        current_sort = self.request.GET.get('sort')

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
        context['sorts'] = {
            'choices': self.sort,
            'current': current_sort,
            'label': SORT_GET_TO_LABEL[current_sort] if current_sort else 'Rating',
        }

        return context

    def player_pagination(self, players):
        paginator = Paginator(self.get_players_queryset(players), self.players_per_page)

        try:
            # Deliver the requested page
            return paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            return paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return paginator.page(paginator.num_pages)

    def get_players_queryset(self, players):
        if self.always_filters:
            players = players.filter(**self.always_filters)

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

        if self.is_sorted():
            sort = self.request.GET.get('sort')
            order = self.request.GET.get('order')

            players = players.order_by(f'{"-" if order != "asc" else ""}{sort}')

            # defer = ['first_name', 'last_name', 'common_name', 'english_names', 'ea_id_base', 'image', 'image_sm',
            # 'image_md', 'image_lg', 'image_special_md_totw', 'image_special_lg_totw', 'position_full',
            # 'position_line', 'play_style', 'play_style_id', 'height', 'weight', 'birth_date', 'acceleration',
            # 'aggression', 'agility', 'balance', 'ball_control', 'crossing', 'curve', 'dribbling', 'finishing',
            # 'free_kick_accuracy', 'heading_accuracy', 'interceptions', 'jumping', 'long_passing', 'long_shots',
            # 'marking', 'penalties', 'positioning', 'potential', 'reactions', 'short_passing', 'shot_power',
            # 'sliding_tackle', 'sprint_speed', 'standing_tackle', 'stamina', 'strength', 'vision', 'volleys',
            # 'gk_diving', 'gk_handling', 'gk_kicking', 'gk_positioning', 'gk_reflexes', 'total_stats',
            # 'total_ingame_stats', 'foot', 'skill_moves', 'weak_foot', 'specialities', 'traits', 'work_rate_att',
            # 'work_rate_def', 'player_type', 'item_type', 'model_name', 'source', 'is_special_type', 'pack_weight',
            # 'created', 'modified']
            # if sort in defer:
            #     defer.remove(sort)

            # players = players.defer(*defer)

        return players

    @property
    def filters(self):
        return {
            'levels': [
                {'key': 'all', 'label': 'All', 'group': False},
                {'key': 'totw', 'label': 'TOTW', 'group': False},
                {'key': 'gold', 'label': 'Gold', 'group': False},
                {'key': 'silver', 'label': 'Silver', 'group': False},
                {'key': 'bronze', 'label': 'Bronze', 'group': False},
                {
                    'key': '', 'label': 'TOTW', 'group': True, 'options': [
                        {'key': 'totw-gold', 'label': 'TOTW Gold'},
                        {'key': 'totw-silver', 'label': 'TOTW Silver'},
                        {'key': 'totw-bronze', 'label': 'TOTW Bronze'},
                    ]
                },
                {
                    'key': '', 'label': 'Rares', 'group': True, 'options': [
                        {'key': 'rare-gold', 'label': 'Rare Gold'},
                        {'key': 'rare-silver', 'label': 'Rare Silver'},
                        {'key': 'rare-bronze', 'label': 'Rare Bronze'},
                    ]
                },
                {
                    'key': '', 'label': 'Non rares', 'group': True, 'options': [
                        {'key': 'nonrare-gold', 'label': 'Gold'},
                        {'key': 'nonrare-silver', 'label': 'Silver'},
                        {'key': 'nonrare-bronze', 'label': 'Bronze'},
                    ]
                },
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
                {
                    'key': '', 'label': 'Positions', 'group': True, 'options': [
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
                    ]
                },
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

    @property
    def sort(self):
        return [
            {'key': 'likes', 'label': 'Likes'},
            {'key': 'rating', 'label': 'Rating'},
            {
                'key': '', 'label': 'Pace', 'group': True, 'options': [
                    {'key': 'acceleration', 'label': 'Acceleration'},
                    {'key': 'sprint_speed', 'label': 'Sprint speed'},
                ]
            },
            {
                'key': '', 'label': 'Shooting', 'group': True, 'options': [
                    {'key': 'finishing', 'label': 'Finishing'},
                    {'key': 'long_shots', 'label': 'Long shots'},
                    {'key': 'penalties', 'label': 'Penalties'},
                    {'key': 'positioning', 'label': 'Positioning'},
                    {'key': 'shot_power', 'label': 'Shot power'},
                    {'key': 'volleys', 'label': 'Volleys'},
                ]
            },
            {
                'key': '', 'label': 'Passing', 'group': True, 'options': [
                    {'key': 'crossing', 'label': 'Crossing'},
                    {'key': 'curve', 'label': 'Curve'},
                    {'key': 'free_kick_accuracy', 'label': 'Free kick'},
                    {'key': 'long_passing', 'label': 'Long passing'},
                    {'key': 'short_passing', 'label': 'Short passing'},
                    {'key': 'vision', 'label': 'Vision'},
                ]
            },
            {
                'key': '', 'label': 'Dribbling', 'group': True, 'options': [
                    {'key': 'agility', 'label': 'Agility'},
                    {'key': 'balance', 'label': 'Balance'},
                    {'key': 'ball_control', 'label': 'Ball control'},
                    {'key': 'dribbling', 'label': 'Dribbling'},
                    {'key': 'reactions', 'label': 'Reactions'},
                ]
            },
            {
                'key': '', 'label': 'Defending', 'group': True, 'options': [
                    {'key': 'heading', 'label': 'Heading'},
                    {'key': 'interceptions', 'label': 'Interceptions'},
                    {'key': 'marking', 'label': 'Marking'},
                    {'key': 'sliding_tackle', 'label': 'Sliding tackle'},
                    {'key': 'standing_tackle', 'label': 'Standing tackle'},
                ]
            },
            {
                'key': '', 'label': 'Physical', 'group': True, 'options': [
                    {'key': 'aggression', 'label': 'Aggression'},
                    {'key': 'jumping', 'label': 'Jumping'},
                    {'key': 'stamina', 'label': 'Stamina'},
                    {'key': 'strength', 'label': 'Strength'},
                ]
            },
            {
                'key': '', 'label': 'Futily', 'group': True, 'options': [
                    {'key': 'rating_attacker', 'label': 'Attacker'},
                    {'key': 'rating_creator', 'label': 'Creator'},
                    {'key': 'rating_defender', 'label': 'Defender'},
                    {'key': 'rating_creative', 'label': 'Pirlo'},
                    {'key': 'rating_beast', 'label': 'Beast'},
                ]
            },
            {'key': 'card_att_1', 'label': 'Pace'},
            {'key': 'card_att_2', 'label': 'Shooting'},
            {'key': 'card_att_3', 'label': 'Passing'},
            {'key': 'card_att_4', 'label': 'Dribbling'},
            {'key': 'card_att_5', 'label': 'Defending'},
            {'key': 'card_att_6', 'label': 'Physical'},
            {'key': 'total_stats', 'label': 'Total stats'},
            {'key': 'total_ingame_stats', 'label': 'Total ingame stats'},
            {'key': 'birth_date', 'label': 'Age'},
        ]


class EaObjectList(ListView):
    def is_sorted(self):
        return self.request.GET.get('sort')

    def get_sort_by(self):
        return self.request.GET.get('sort')

    def get_queryset(self):
        qs = super().get_queryset()

        if self.is_sorted():
            sort_by = self.get_sort_by()

            schema = {
                'avg': 'average_rating',
                'total': 'total_players',
                'golds': 'total_gold',
                'silvers': 'total_silver',
                'bronzes': 'total_bronze',
                '-avg': '-average_rating',
                '-total': '-total_players',
                '-golds': '-total_gold',
                '-silvers': '-total_silver',
                '-bronzes': '-total_bronze',
            }

            if 'ifs' in sort_by:
                qs = qs.order_by(F('total_totw') + F('total_special'))

                if '-' in sort_by:
                    qs = qs.reverse()
            elif sort_by in schema:
                qs = qs.order_by(schema[sort_by])

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_sort = self.get_sort_by()

        context['titles'] = []

        for title in ['avg', 'total', 'golds', 'silvers', 'bronzes', 'ifs']:
            label = title
            key = '-{}'.format(title)
            current = False

            if current_sort and title in current_sort:
                key = title if current_sort[0] == '-' else '-{}'.format(title)
                current = True

            context['titles'].append({
                'label': label,
                'key': key,
                'current': current,
            })

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
