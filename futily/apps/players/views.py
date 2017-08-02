from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import PlayerListForm
from .models import Player


class PlayerList(FormMixin, ListView):
    form_class = PlayerListForm
    model = Player
    paginate_by = 30
    success_url = '/'

    def get_initial(self):
        initial = super(PlayerList, self).get_initial()

        initial.update(self.request.GET)

        return initial

    def get_queryset(self):  # pylint: disable=too-complex, too-many-locals
        qs = super(PlayerList, self).get_queryset()

        current_filters = self.request.GET
        allowed_filters = self.allowed_filters()

        # Check if we have any filterable parameters
        if current_filters and set(current_filters.dict().keys()).issubset(set(allowed_filters)):
            if current_filters.get('min_rating') and current_filters.get('max_rating'):
                qs = qs.filter(rating__range=(current_filters.get('min_rating'), current_filters.get('max_rating')))

            if current_filters.get('position'):
                # If the value of this == 'all' then check the form submission in JS and clear this value if need be
                # Alternatively remove the 'all' option and just rely on the "clear" to remove it
                current_positions = current_filters.getlist('position')
                individual_positions = Player.objects.order_by('position').values_list('position', flat=True).distinct()
                line_positions = Player.objects.order_by('position_line').values_list('position_line', flat=True).distinct()
                position_schema = {x.lower(): {'position__in': [x.upper()]} for x in individual_positions}
                position_schema.update({x.lower(): {'position_line__in': [x.upper()]} for x in line_positions})
                position_schema.update({
                    'cbs': {'position__in': ['CB']},
                    'rbs': {'position__in': ['RB', 'RWB']},
                    'lbs': {'position__in': ['LB', 'LWB']},
                    'cms': {'position__in': ['CDM', 'CM', 'CAM']},
                    'rms': {'position__in': ['RM', 'RW', 'RF']},
                    'lms': {'position__in': ['LM', 'LW', 'LF']},
                    'sts': {'position__in': ['CF', 'ST']},
                })

                position_filter = construct_query_dict(current_positions, position_schema)
                queries = [Q(**{key: value}) for key, value in position_filter.items()]
                query = queries.pop()

                for item in queries:
                    query |= item

                qs = qs.filter(query)

            if current_filters.get('level'):
                current_levels = current_filters.getlist('level')
                available_levels = Player.objects.order_by('color').values_list('color', flat=True).distinct()
                gold_levels = [x for x in available_levels if 'gold' in x]
                silver_levels = [x for x in available_levels if 'silver' in x]
                bronze_levels = [x for x in available_levels if 'bronze' in x]
                special_levels = [x for x in available_levels if x not in gold_levels + silver_levels + bronze_levels]
                level_schema = {
                    'legend': {'color__in': [x for x in available_levels if 'legend' in x]},
                    'special': {'color__in': special_levels},
                    'gold': {'color__in': gold_levels},
                    'silver': {'color__in': silver_levels},
                    'bronze': {'color__in': bronze_levels},
                    'totw_all': {'color__in': [
                        x for x in bronze_levels + silver_levels + gold_levels if 'totw' in x]},
                    'totw_gold': {'color__in': [x for x in gold_levels if 'totw' in x]},
                    'totw_silver': {'color__in': [x for x in silver_levels if 'totw' in x]},
                    'totw_bronze': {'color__in': [x for x in bronze_levels if 'totw' in x]},
                    'gold_rare': {'color__in': [x for x in gold_levels if 'rare' in x]},
                    'gold_common': {'color__in': ['gold']},
                    'silver_rare': {'color__in': [x for x in silver_levels if 'rare' in x]},
                    'silver_common': {'color__in': ['silver']},
                    'bronze_rare': {'color__in': [x for x in bronze_levels if 'rare' in x]},
                    'bronze_common': {'color__in': ['bronze']},
                    'award_winner': {'color__in': ['award_winner']},
                    'confederation_champions_motm': {'color__in': ['confederation_champions_motm']},
                    'fut_birthday': {'color__in': ['fut_birthday']},
                    'gotm': {'color__in': ['gotm']},
                    'halloween': {'color__in': ['halloween']},
                    'imotm': {'color__in': ['imotm']},
                    'motm': {'color__in': ['motm']},
                    'movember': {'color__in': ['movember']},
                    'ones_to_watch': {'color__in': ['ones_to_watch']},
                    'purple': {'color__in': ['purple']},
                    'record_breaker': {'color__in': ['record_breaker']},
                    'sbc_base': {'color__in': ['sbc_base']},
                    'st_patricks': {'color__in': ['st_patricks']},
                    'tots': {'color__in': ['tots']},
                    'toty': {'color__in': ['toty']},
                }

                color_filter = construct_query_dict(current_levels, level_schema)

                qs = qs.filter(**color_filter)

            if current_filters.get('nation'):
                qs = qs.filter(nation__slug__in=current_filters.getlist('nation'))

            if current_filters.get('league'):
                qs = qs.filter(league__slug__in=current_filters.getlist('league'))

            if current_filters.get('skills'):
                qs = qs.filter(skill_moves=current_filters.get('skills'))

            if current_filters.get('weak_foot'):
                qs = qs.filter(weak_foot=current_filters.get('weak_foot'))

            if current_filters.get('def_workrate'):
                qs = qs.filter(work_rate_def=current_filters.get('def_workrate').title())

            if current_filters.get('att_workrate'):
                qs = qs.filter(work_rate_att=current_filters.get('att_workrate').title())

            if current_filters.get('strong_foot'):
                qs = qs.filter(foot=current_filters.get('strong_foot').title())

        return qs

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        return super(PlayerList, self).get_context_data(**kwargs)

    def allowed_filters(self):
        form = self.get_form()

        return [x.html_name for x in form]


class PlayerDetail(DetailView):
    model = Player


class PlayerDetailChemistry(DetailView):
    model = Player
    template_name = 'players/player_detail_chemistry.html'


class PlayerDetailChemistryType(DetailView):
    model = Player
    template_name = 'players/player_detail_chemistry_type.html'

    def player_pagination(self, qs):
        paginator = Paginator(qs, 36)

        try:
            # Deliver the requested page
            return paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            return paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return paginator.page(paginator.num_pages)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['players'] = self.player_pagination(self.object.get_chemistry_players()[self.kwargs['chem_type']])

        return context


class PlayerDetailSimilar(DetailView):
    model = Player
    template_name = 'players/player_detail_similar.html'

    def player_pagination(self):
        paginator = Paginator(self.object.get_similar_players(), 36)

        try:
            # Deliver the requested page
            return paginator.page(self.request.GET.get('page'))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            return paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            return paginator.page(paginator.num_pages)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['similar_coefficient'] = self.object.similar_coefficient
        context['similar_players'] = self.player_pagination()

        return context


def construct_query_dict(current, schema):
    filter_dict = {}
    wanted = []

    for position in current:
        wanted.append(schema[position])

    for color in wanted:
        for key, value in color.items():
            if key not in filter_dict:
                filter_dict[key] = value
            elif key in filter_dict:
                filter_dict[key] += value
                filter_dict[key] = list(set(filter_dict[key]))

    return filter_dict
