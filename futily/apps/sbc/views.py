from collections import OrderedDict

from django.db.models import Prefetch
from django.views.generic import DetailView, ListView

from futily.apps.sbc.models import (SquadBuilderChallenge,
                                    SquadBuilderChallengeAward,
                                    SquadBuilderChallengeCategory,
                                    SquadBuilderChallengeSet,
                                    SquadBuildingChallenges)
from futily.apps.squads.constants import FORMATION_POSITIONS
from futily.apps.squads.models import FORMATION_CHOICES


class SquadBuilderChallengeBase(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = [
            {
                'label': x.title,
                'url': x.get_absolute_url(),
                'here': x.get_absolute_url() in self.request.path and self.request.path != SquadBuildingChallenges.objects.first().page.get_absolute_url(),
            } for x in SquadBuilderChallengeCategory.objects.all()
        ]

        context['categories'] = [{
            'label': 'All',
            'url': SquadBuildingChallenges.objects.first().page.get_absolute_url(),
            'here': self.request.path in SquadBuildingChallenges.objects.first().page.get_absolute_url()
        }] + categories

        return context


class SquadBuilderChallengeSetList(SquadBuilderChallengeBase, ListView):
    model = SquadBuilderChallengeSet
    template_name = 'sbc/set_list.html'


class SquadBuilderChallengeCategoryView(SquadBuilderChallengeBase, ListView):
    model = SquadBuilderChallengeSet
    template_name = 'sbc/set_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('category'))


class SquadBuilderChallengeSetDetail(SquadBuilderChallengeBase, DetailView):
    model = SquadBuilderChallengeSet
    template_name = 'sbc/set_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        def build_dict(seq, key):
            return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

        category = build_dict(context['categories'], 'label')[self.object.category.title]
        del category['index']
        index = context['categories'].index(category)
        context['categories'][index]['here'] = True

        return context


class SquadBuilderChallengeDetail(SquadBuilderChallengeBase, DetailView):
    model = SquadBuilderChallenge
    template_name = 'sbc/challenge_detail.html'

    def get_object(self, queryset=None):
        return self.model.objects.prefetch_related('awards', 'requirements').get(
            set__slug=self.kwargs.get('set_slug'),
            slug=self.kwargs.get('slug')
        )


class SquadBuilderChallengeBuilder(SquadBuilderChallengeBase, DetailView):
    model = SquadBuilderChallenge
    template_name = 'sbc/challenge_builder.html'

    def get_object(self, queryset=None):
        return self.model.objects.prefetch_related('awards', 'requirements').get(
            set__slug=self.kwargs.get('set_slug'),
            slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['formations'] = dict(OrderedDict(FORMATION_CHOICES))
        context['FORMATION_POSITIONS'] = FORMATION_POSITIONS[self.object.formation]

        return context
