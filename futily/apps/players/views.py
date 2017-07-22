from django.views.generic import DetailView, ListView

from .models import Player


class PlayerList(ListView):
    model = Player
    paginate_by = 50


class PlayerDetail(DetailView):
    model = Player
