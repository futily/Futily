import json
from collections import OrderedDict

from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.generic import DetailView, FormView, ListView

from futily.apps.actions.utils import create_action
from futily.apps.sbc.models import (SquadBuilderChallenge,
                                    SquadBuilderChallengeCategory,
                                    SquadBuilderChallengeSet,
                                    SquadBuildingChallenges)
from futily.apps.squads.constants import FORMATION_POSITIONS
from futily.apps.squads.forms import SBCBuilderForm
from futily.apps.squads.models import (FORMATION_CHOICES, Squad, SquadPlayer,
                                       get_default_squad_page)
from futily.apps.views import BreadcrumbsMixin
from futily.utils.functions import static


class SquadBuilderChallengeBase(BreadcrumbsMixin):
    def set_breadcrumbs(self):
        return [
            {
                'label': 'Squad building challenges',
                'link': self.request.pages.current.get_absolute_url(),
            }
        ]

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


class SquadBuilderChallengeSetDetail(SquadBuilderChallengeBase, DetailView):
    model = SquadBuilderChallengeSet
    template_name = 'sbc/set_detail.html'

    def set_breadcrumbs(self):
        category = SquadBuilderChallengeCategory.objects.get(slug=self.object.category.slug)

        return super(SquadBuilderChallengeSetDetail, self).set_breadcrumbs() + [
            {
                'label': category.title,
                'link': category.get_absolute_url(),
            },
            {
                'label': self.object,
                'link': self.object.get_absolute_url(),
                'image': static(f'ea-images/sbc/sets/{self.object.trophy_id}.png')
            }
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        def build_dict(seq, key):
            return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

        category = build_dict(context['categories'], 'label')[self.object.category.title]
        del category['index']
        index = context['categories'].index(category)
        context['categories'][index]['here'] = True

        return context


class SquadBuilderChallengeCategoryView(SquadBuilderChallengeBase, ListView):
    model = SquadBuilderChallengeSet
    template_name = 'sbc/set_list.html'

    def set_breadcrumbs(self):
        category = SquadBuilderChallengeCategory.objects.get(slug=self.kwargs.get('category'))

        return super(SquadBuilderChallengeCategoryView, self).set_breadcrumbs() + [
            {
                'label': category.title,
                'link': category.get_absolute_url(),
            }
        ]

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('category'))


class SquadBuilderChallengeDetail(SquadBuilderChallengeBase, DetailView):
    model = SquadBuilderChallenge
    template_name = 'sbc/challenge_detail.html'

    def set_breadcrumbs(self):
        category = SquadBuilderChallengeCategory.objects.get(slug=self.object.set.category.slug)

        return super(SquadBuilderChallengeDetail, self).set_breadcrumbs() + [
            {
                'label': category.title,
                'link': category.get_absolute_url(),
            },
            {
                'label': self.object.set,
                'link': self.object.set.get_absolute_url(),
                'image': static(f'ea-images/sbc/sets/{self.object.set.trophy_id}.png'),
            },
            {
                'label': self.object,
                'link': self.object.get_absolute_url(),
                'image': static(f'ea-images/sbc/challenges/{self.object.trophy_id}.png'),
            },
        ]

    def get_object(self, queryset=None):
        return self.model.objects.prefetch_related(
            Prefetch('squad_set', queryset=Squad.objects.all(), to_attr='sbc'),
            'awards',
            'requirements'
        ).get(
            set__slug=self.kwargs.get('set_slug'),
            slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        def build_dict(seq, key):
            return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

        category = build_dict(context['categories'], 'label')[self.object.set.category.title]
        del category['index']
        index = context['categories'].index(category)
        context['categories'][index]['here'] = True

        return context


class SquadBuilderChallengeBuilder(SquadBuilderChallengeBase, DetailView):
    model = SquadBuilderChallenge
    template_name = 'sbc/challenge_builder.html'

    def set_breadcrumbs(self):
        category = SquadBuilderChallengeCategory.objects.get(slug=self.object.set.category.slug)

        return super(SquadBuilderChallengeBuilder, self).set_breadcrumbs() + [
            {
                'label': category.title,
                'link': category.get_absolute_url(),
            },
            {
                'label': self.object.set,
                'link': self.object.set.get_absolute_url(),
                'image': static(f'ea-images/sbc/sets/{self.object.set.trophy_id}.png'),
            },
            {
                'label': self.object,
                'link': self.object.get_absolute_url(),
                'image': static(f'ea-images/sbc/challenges/{self.object.trophy_id}.png'),
            },
            {
                'label': 'Builder',
                'link': self.request.pages.current.reverse('challenge_builder', kwargs={
                    'set_slug': self.object.set.slug,
                    'slug': self.object.slug,
                }),
            },
        ]

    def get_object(self, queryset=None):
        return self.model.objects.prefetch_related('awards', 'requirements').get(
            set__slug=self.kwargs.get('set_slug'),
            slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['squads_page_id'] = get_default_squad_page().pk
        context['formations'] = dict(OrderedDict(FORMATION_CHOICES))
        context['FORMATION_POSITIONS'] = FORMATION_POSITIONS[self.object.formation]
        context['awards_json'] = json.dumps([
            x.to_json_string for x in self.object.awards.all()
        ])
        context['requirements_json'] = json.dumps([
            x.to_json_string for x in self.object.requirements.all()
        ])
        context['user_data'] = json.dumps({
            'id': self.request.user.id,
            'username': self.request.user.username,
            'link': self.request.user.get_absolute_url(),
        }) if self.request.user.is_authenticated else json.dumps({
            'id': None,
            'username': None,
            'link': None
        })

        return context


class SquadBuilderChallengeSave(FormView):
    model = SquadBuilderChallenge

    def get_object(self):
        return self.model.objects.get(
            set__slug=self.kwargs.get('set_slug'),
            slug=self.kwargs.get('slug')
        )

    def post(self, request, *args, **kwargs):
        form = SBCBuilderForm(self.request.POST)

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
                create_action(request.user, f'created squad for SBC {self.get_object().title}', squad)

        response_data['url'] = squad.get_absolute_url()

        return JsonResponse(response_data, status=200)
