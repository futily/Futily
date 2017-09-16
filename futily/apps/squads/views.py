import json
import urllib
from collections import OrderedDict

from django.http import JsonResponse
from django.utils.text import slugify
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import TemplateView, View

from futily.apps.actions.utils import create_action
from futily.apps.players.models import Player

from .forms import BuilderForm
from .models import FORMATION_CHOICES, Squad, SquadPlayer


class Builder(TemplateView):
    model = Squad
    template_name = 'squads/squad_builder.html'

    fields = ['players', 'formation', 'chemistry', 'rating', 'attack', 'midfield', 'defence',
              'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']

    def get_context_data(self, **kwargs):
        context = super(Builder, self).get_context_data(**kwargs)

        context['formations'] = dict(OrderedDict(FORMATION_CHOICES))

        return context


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
            squad = Squad(**form.cleaned_data)
            squad.save()

            if form.cleaned_data.get('players'):
                players = form.cleaned_data.pop('players')

                for player in players:
                    p = SquadPlayer(player=player[0], squad=squad, index=player[1], position=player[2])
                    p.save()

            create_action(request.user, 'created squad', squad)

        return JsonResponse(response_data)


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

    def get_queryset(self):
        print(Squad.objects.all())

        return super(SquadList, self).get_queryset().filter(page__page=self.request.pages.current)


class SquadDetail(DetailView):
    model = Squad
