from django.views.generic import DetailView, ListView

from .models import Club


class ClubList(ListView):
    model = Club
    paginate_by = 50


class ClubDetail(DetailView):
    model = Club
