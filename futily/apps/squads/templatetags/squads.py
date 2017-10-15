from django_jinja import library

from futily.apps.squads.models import Squads


@library.global_function
def get_squads_page():
    return Squads.objects.first().page
