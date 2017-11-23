from django.views.generic import DetailView
from rest_framework import filters, viewsets

from futily.apps.clubs.serializers import ClubSerializer

from ..views import BreadcrumbsMixin, EaObjectList
from .models import Club


class ClubList(EaObjectList):
    model = Club
    paginate_by = 50


class ClubDetail(BreadcrumbsMixin, DetailView):
    model = Club

    def set_breadcrumbs(self):
        return [
            {
                'label': self.object._meta.app_label.title(),
                'link': self.request.pages.current.get_absolute_url(),
            },
            {
                'label': self.object,
            },
        ]


class ClubViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get('query')

        if query:
            qs = qs.filter(name__icontains=query)

        return qs
