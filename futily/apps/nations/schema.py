from graphene import Int, Node, relay
from graphene_django import DjangoConnectionField, DjangoObjectType

from .models import Nation


class NationNode(DjangoObjectType):

    class Meta:
        model = Nation
        interfaces = [relay.Node]
        only_fields = ['title', 'ea_id']


class NationConnection(relay.Connection):
    class Meta:
        node = NationNode


class Query(object):
    nations = DjangoConnectionField(NationNode, enforce_first_or_last=True)
    nations_connection = relay.ConnectionField(NationConnection)
    nation = Node.Field(NationNode, id=Int())

    node = relay.Node.Field()

    def resolve_nations(self, *args, **kwargs):
        return Nation.objects.all()

    def resolve_nation(self, info, **kwargs):
        _id = kwargs.get('id')

        if _id is not None:
            return Nation.objects.get(pk=_id)

        return None
