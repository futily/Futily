from graphene import Int, Node, relay
from graphene_django import DjangoConnectionField, DjangoObjectType

from .models import League


class LeagueNode(DjangoObjectType):

    class Meta:
        model = League
        interfaces = [relay.Node]
        only_fields = ['title', 'ea_id']


class LeagueConnection(relay.Connection):
    class Meta:
        node = LeagueNode


class Query(object):
    leagues = DjangoConnectionField(LeagueNode, enforce_first_or_last=True)
    leagues_connection = relay.ConnectionField(LeagueConnection)
    league = Node.Field(LeagueNode, id=Int())

    node = relay.Node.Field()

    def resolve_leagues(self, *args, **kwargs):
        return League.objects.all()

    def resolve_league(self, info, **kwargs):
        _id = kwargs.get('id')

        if _id is not None:
            return League.objects.get(pk=_id)

        return None
