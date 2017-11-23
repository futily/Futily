from rest_framework import filters, viewsets

from futily.apps.nations.serializers import NationSerializer
from futily.apps.views import EaObjectDetail, EaObjectList, PlayerFilterSorted

from .models import Nation


class NationList(EaObjectList):
    paginate_by = 50
    model = Nation


class NationDetail(EaObjectDetail, PlayerFilterSorted):
    model = Nation

    def initial_players(self):
        return self.object.players()


class NationViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Nation.objects.all()
    serializer_class = NationSerializer
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get('query')

        if query:
            qs = qs.filter(name__icontains=query)

        return qs
