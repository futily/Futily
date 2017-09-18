from django.views.generic import DetailView

from ..views import EaObjectList, PlayerFilterSorted
from .models import Nation


class NationList(EaObjectList):
    paginate_by = 50
    model = Nation


class NationDetail(DetailView, PlayerFilterSorted):
    model = Nation

    def initial_players(self):
        return self.object.players()
