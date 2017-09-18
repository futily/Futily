from django.views.generic import DetailView

from ..views import EaObjectList
from .models import Club


class ClubList(EaObjectList):
    model = Club
    paginate_by = 50


class ClubDetail(DetailView):
    model = Club
