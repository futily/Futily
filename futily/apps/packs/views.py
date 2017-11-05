import random

from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from futily.apps.actions.utils import create_action
from futily.apps.players.constants import SPECIAL_COLOR_CHOICES
from futily.apps.users.models import CollectionPlayer

from ..players.models import Player
from .forms import PackCreationForm
from .models import Pack, PackType


class PackLeaderboard(ListView):
    model = Pack
    ordering = ['-value']
    paginate_by = 50
    template_name = 'packs/pack_leaderboard.html'


class TypeList(ListView):
    model = PackType
    queryset = PackType.objects.filter(show_in_list=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object_list'] = {
            'bronze': {
                'title': 'Bronze',
                'types': self.get_queryset().filter(type='bronze'),
            },
            'silver': {
                'title': 'Silver',
                'types': self.get_queryset().filter(type='silver'),
            },
            'gold': {
                'title': 'Gold',
                'types': self.get_queryset().filter(type='gold'),
            },
            'special': {
                'title': 'Special',
                'types': self.get_queryset().filter(type='special'),
            },
        }
        context['type_list'] = context['object_list']

        return context


class TypeDetail(FormMixin, DetailView):
    model = PackType
    form_class = PackCreationForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pack_object = None

    def roll_querysets(self):
        def map_rolls(roll):
            roll_schema = {
                '1': (0, 360),
                '2': (361, 569),
                '3': (570, 600),
                '4': (601, 959),
                '5': (960, 994),
                '6': (995, 1000),
            }

            for k, v in roll_schema.items():
                if v[0] <= roll <= v[1]:
                    return k

        rare_schema = {
            'bronze': {
                '1': {
                    'color__in': ['rare_bronze'],
                    'rating__range': (46, 60),
                },
                '2': {
                    'color__in': ['rare_bronze'],
                    'rating__range': (46, 61),
                },
                '3': {
                    'color__in': ['rare_bronze'],
                    'rating__range': (46, 62),
                },
                '4': {
                    'color__in': ['rare_bronze'],
                    'rating__range': (46, 64),
                },
                '5': {
                    'color__in': ['rare_bronze', 'rare_silver', 'totw_bronze'],
                    'rating__range': (60, 64),
                },
                '6': {
                    'color__in': ['rare_bronze', 'rare_silver', 'totw_bronze', 'totw_silver', 'tots_bronze'],
                    'rating__range': (63, 64)
                },
            },
            'silver': {
                '1': {
                    'color__in': ['rare_silver'],
                    'rating__range': (65, 70),
                },
                '2': {
                    'color__in': ['rare_silver'],
                    'rating__range': (65, 71),
                },
                '3': {
                    'color__in': ['rare_silver'],
                    'rating__range': (65, 72),
                },
                '4': {
                    'color__in': ['rare_silver'],
                    'rating__range': (65, 74),
                },
                '5': {
                    'color__in': ['rare_silver', 'totw_silver'],
                    'rating__range': (70, 74),
                },
                '6': {
                    'color__in': ['rare_bronze', 'rare_silver', 'totw_silver', 'tots_silver', 'rare_gold'],
                    'rating__range': (73, 74),
                },
            },
            'gold': {
                '1': {
                    'color__in': ['rare_gold'],
                    'rating__range': (75, 80),
                },
                '2': {
                    'color__in': ['rare_gold'],
                    'rating__range': (75, 81),
                },
                '3': {
                    'color__in': ['rare_gold'],
                    'rating__range': (75, 82),
                },
                '4': {
                    'color__in': ['rare_gold'],
                    'rating__range': (75, 83),
                },
                '5': {
                    'color__in': ['rare_gold', 'totw_gold', 'legend'],
                    'rating__range': (81, 90),
                },
                '6': {
                    'color__in': ['rare_silver', 'rare_gold', 'legend'] + [x[0] for x in SPECIAL_COLOR_CHOICES],
                    'rating__range': (83, 99),
                },
            },
        }

        leftover_schema = {
            'bronze': {
                '1': (46, 60),
                '2': (46, 60),
                '3': (46, 60),
                '4': (55, 62),
                '5': (60, 63),
                '6': (62, 63),
            },
            'silver': {
                '1': (65, 70),
                '2': (65, 70),
                '3': (65, 70),
                '4': (68, 72),
                '5': (71, 73),
                '6': (72, 73),
            },
            'gold': {
                '1': (75, 82),
                '2': (75, 82),
                '3': (75, 82),
                '4': (78, 82),
                '5': (80, 83),
                '6': (83, 84),
            },
        }

        rare_rolls = [map_rolls(random.randint(1, 1000)) for _ in range(self.object.rare_count)]
        rare_players = [Player.objects.order_by('?').filter(
            **rare_schema[self.object.type][x]
        ).first() for x in rare_rolls]

        type_left = getattr(self.object, f'{self.object.type}_count') - \
            len([x for x in rare_players if self.object.type in x.color])
        type_rolls = [map_rolls(random.randint(1, 1000)) for _ in
                      range(type_left)]

        type_players = [Player.objects.order_by('?').filter(
            color=self.object.type,
            rating__range=[leftover_schema[self.object.type][x][0], leftover_schema[self.object.type][x][1]]
        ).first() for x in type_rolls]

        leftover_rolls = [map_rolls(random.randint(1, 1000)) for _ in
                          range(self.object.total_count - len(rare_players + type_players))]
        leftover_players = [Player.objects.order_by('?').filter(
            color=self.object.type,
            rating__range=[leftover_schema[self.object.type][x][0], leftover_schema[self.object.type][x][1]]
        ).first() for x in leftover_rolls]

        players = rare_players + type_players + leftover_players
        random.shuffle(players)

        return players

    def get_success_url(self):
        return self.pack_object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(TypeDetail, self).get_context_data(**kwargs)

        context['form'] = PackCreationForm()
        context['players'] = self.roll_querysets()
        context['value'] = sum([x.pack_value for x in context['players']])
        context['new_players'] = []

        if self.request.user.is_authenticated:
            for player in context['players']:
                obj, created = CollectionPlayer.objects.get_or_create(
                    collection=self.request.user.cardcollection, player=player)

                if not created:
                    obj.count += 1
                    obj.save()
                else:
                    context['new_players'].append(player)

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        self.pack_object = form.save()

        create_action(self.request.user, 'saved a pack', self.pack_object)

        return super(TypeDetail, self).form_valid(form)


class PackDetail(DetailView):
    model = Pack
