from django.views.generic import DetailView, ListView

from .models import Nation


class NationList(ListView):
    model = Nation
    paginate_by = 50


class NationDetail(DetailView):
    model = Nation
