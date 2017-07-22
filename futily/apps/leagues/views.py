from ..views import EaObjectDetail, EaObjectList
from .models import League


class LeagueList(EaObjectList):
    model = League
    paginate_by = 50


class LeagueDetail(EaObjectDetail):
    model = League
