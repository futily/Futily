from django.utils.text import slugify
from rest_framework import filters, viewsets

from futily.apps.players.models import Player
from futily.apps.players.serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_fields = ['first_name', 'last_name', 'common_name']

    def get_queryset(self):
        query = self.request.query_params.get('query')
        ids = None

        if self.request.query_params.get('ids'):
            ids = self.request.query_params.get('ids').split(',')[:-1]

        qs = Player.objects.all()

        if ids:
            qs = qs.filter(ea_id_base__in=ids)

        if query:
            qs = qs.filter(english_names__icontains=query)

        nation = self.request.query_params.get('nation')

        if nation:
            qs = qs.filter(nation__slug=slugify(nation))

        return qs
