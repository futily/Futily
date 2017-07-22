from django.db.models import F
from django.views.generic import ListView

from ..views import EaObjectDetailView
from .models import Nation


class NationList(ListView):
    model = Nation
    paginate_by = 50

    def is_sorted(self):
        return self.request.GET.get('sort')

    def get_sort_by(self):
        return self.request.GET.get('sort')

    def get_queryset(self):
        qs = super().get_queryset()

        if self.is_sorted():
            sort_by = self.get_sort_by()

            schema = {
                'avg': 'average_rating',
                'total': 'total_players',
                'golds': 'total_gold',
                'silvers': 'total_silver',
                'bronzes': 'total_bronze',
                '-avg': '-average_rating',
                '-total': '-total_players',
                '-golds': '-total_gold',
                '-silvers': '-total_silver',
                '-bronzes': '-total_bronze',
            }

            if 'ifs' in sort_by:
                qs = qs.order_by(F('total_totw') + F('total_special'))

                if '-' in sort_by:
                    qs = qs.reverse()
            elif sort_by in schema:
                qs = qs.order_by(schema[sort_by])

        return qs

    def get_context_data(self, **kwargs):
        context = super(NationList, self).get_context_data(**kwargs)
        current_sort = self.get_sort_by()

        context['titles'] = []

        for title in ['avg', 'total', 'golds', 'silvers', 'bronzes', 'ifs']:
            label = title
            key = '-{}'.format(title)
            current = False

            if current_sort and title in current_sort:
                key = title if current_sort[0] == '-' else '-{}'.format(title)
                current = True

            context['titles'].append({
                'label': label,
                'key': key,
                'current': current,
            })

        return context


class NationDetail(EaObjectDetailView):
    model = Nation
