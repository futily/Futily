from django.views.generic import DetailView

from ..views import EaObjectList, PlayerFilterSorted
from .models import League


class LeagueList(EaObjectList):
    model = League
    paginate_by = 50


class LeagueDetail(DetailView, PlayerFilterSorted):
    model = League

    def initial_players(self):
        return self.object.players()
