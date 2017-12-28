from graphene import Int, Node, relay
from graphene_django import DjangoConnectionField, DjangoObjectType

from .models import Club


class ClubNode(DjangoObjectType):

    class Meta:
        model = Club
        interfaces = [relay.Node]
        only_fields = ['title', 'ea_id']


class ClubConnection(relay.Connection):
    class Meta:
        node = ClubNode


class Query(object):
    clubs = DjangoConnectionField(ClubNode, enforce_first_or_last=True)
    clubs_connection = relay.ConnectionField(ClubConnection)
    club = Node.Field(ClubNode, id=Int())

    node = relay.Node.Field()

    def resolve_clubs(self, *args, **kwargs):
        return Club.objects.all()

    def resolve_club(self, info, **kwargs):
        _id = kwargs.get('id')

        if _id is not None:
            return Club.objects.get(pk=_id)

        return None
