from django.db import models
from django_filters import CharFilter, FilterSet
from graphene import (Field, Int, List, ObjectType, Schema, String, relay,
                      resolve_only_args)
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django_extras import (DjangoListObjectField,
                                    DjangoListObjectType, DjangoObjectField,
                                    DjangoSerializerType,
                                    LimitOffsetGraphqlPagination,
                                    get_all_directives)

from futily.apps.clubs.models import Club
from futily.apps.leagues.models import League
from futily.apps.nations.models import Nation
from futily.apps.players.models import Player


class PlayerType(DjangoObjectType):
    pk = Field(Int)
    url = Field(String)
    stats = List(List(String))
    english_names = List(String)
    color = Field(String)
    work_rate_att = Field(String)
    work_rate_def = Field(String)

    class Meta:
        model = Player
        filter_fields = {
            'english_names': ['contains']
        }
        interfaces = [relay.Node]
        only_fields = [
            'pk',
            'stats',
            'club',
            'league',
            'nation',
            'ea_id',
            'ea_id_base',
            'color',
            'rating',
            'position',
            'name',
            'english_names',
            'card_att_1',
            'card_att_2',
            'card_att_3',
            'card_att_4',
            'card_att_5',
            'card_att_6',
            'work_rate_att',
            'work_rate_def',
            'skill_moves',
            'weak_foot',
            'rating_defensive',
            'rating_anchor',
            'rating_creative',
            'rating_attacking']

    @classmethod
    def get_node(cls, info, _id):
        return Player.objects.get(id=_id)

    def resolve_url(instance, info, **kwargs):
        return instance.get_absolute_url()

    def resolve_stats(instance, info, **kwargs):
        return instance.card_stats


class PlayerFilter(FilterSet):
    english_names = CharFilter(method='filter_english_names')

    def filter_english_names(self, queryset, name, value):
        return queryset.filter(
            english_names__icontains=value
        )


class PlayerConnection(relay.Connection):
    class Meta:
        node = PlayerType


class Query(object):
    players = DjangoFilterConnectionField(PlayerType, filterset_class=PlayerFilter, enforce_first_or_last=True)
    player = Field(PlayerType, id=Int())
    players_connection = relay.ConnectionField(PlayerConnection)

    node = relay.Node.Field()

    def resolve_players(self, *args, **kwargs):
        return Player.objects.all()

    def resolve_player(self, info, **kwargs):
        _id = kwargs.get('id')

        if _id is not None:
            return Player.objects.get(pk=_id)

        return None
