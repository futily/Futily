from ..views import EaObjectDetail, EaObjectList
from .models import Nation


class NationList(EaObjectList):
    model = Nation
    paginate_by = 50


class NationDetail(EaObjectDetail):
    model = Nation
