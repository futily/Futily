from ..views import EaObjectDetail, EaObjectList
from .models import Club


class ClubList(EaObjectList):
    model = Club
    paginate_by = 50


class ClubDetail(EaObjectDetail):
    model = Club
