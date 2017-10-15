from django_jinja import library

from futily.apps.leagues.models import Leagues


@library.global_function
def get_leagues_page():
    return Leagues.objects.first().page
