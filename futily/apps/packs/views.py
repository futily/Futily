import random
from collections import Counter

from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from futily.apps.actions.utils import create_action
from futily.apps.users.models import CollectionPlayer

from ..players.models import Player
from .forms import PackCreationForm
from .models import Pack, PackType


class TypeList(ListView):
    model = PackType

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object_list'] = {
            'bronze': {
                'title': 'Bronze packs',
                'types': self.get_queryset().filter(quality='bronze'),
            },
            'silver': {
                'title': 'Silver packs',
                'types': self.get_queryset().filter(quality='silver'),
            },
            'gold': {
                'title': 'Gold packs',
                'types': self.get_queryset().filter(quality='gold'),
            },
            'special': {
                'title': 'Special packs',
                'types': self.get_queryset().filter(quality='special'),
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
                '4': (601, 9559),
                '5': (960, 994),
                '6': (995, 1000),
            }

            for k, v in roll_schema.items():
                if v[0] <= roll <= v[1]:
                    return k

        def map_roll_querysets(roll_count):
            roll, count = roll_count
            min_rating = getattr(self.object, f'roll_{roll}_types_rating_min')
            max_rating = getattr(self.object, f'roll_{roll}_types_rating_max')
            types = getattr(self.object, f'roll_{roll}_types')

            qs = Player.cards.filter(
                rating__range=[min_rating, max_rating]
            ).filter(
                color__in=types
            ).order_by(
                '?'
            )[:count]

            return qs if qs else None

        low_rolls = [random.randint(1, 600) for x in range(self.object.normal_count)]
        high_rolls = [random.randint(601, 1000) for x in range(self.object.rare_count)]
        rolls = low_rolls + high_rolls
        mapped_rolls = list(map(map_rolls, rolls))
        roll_counts = Counter(mapped_rolls)

        players = Player.objects.none()
        querysets = list(x for x in map(map_roll_querysets, roll_counts.items()) if x is not None)

        return players.union(*querysets)

    def get_success_url(self):
        return self.pack_object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(TypeDetail, self).get_context_data(**kwargs)

        context['form'] = PackCreationForm()
        context['players'] = self.roll_querysets()

        if self.request.user.is_authenticated:
            for player in context['players']:
                obj, created = CollectionPlayer.objects.get_or_create(
                    collection=self.request.user.cardcollection, player=player)

                if not created:
                    obj.count += 1
                    obj.save()

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
