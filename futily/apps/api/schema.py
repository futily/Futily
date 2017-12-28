from graphene import ObjectType, Schema

from futily.apps.clubs.schema import Query as ClubsQuery
from futily.apps.leagues.schema import Query as LeaguesQuery
from futily.apps.nations.schema import Query as NationsQuery
from futily.apps.players.schema import Query as PlayersQuery


class Query(ClubsQuery, LeaguesQuery, NationsQuery, PlayersQuery, ObjectType):
    pass


schema = Schema(query=Query)
