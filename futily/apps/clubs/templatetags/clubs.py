from django_jinja import library

from futily.apps.clubs.models import Clubs


@library.global_function
def get_clubs_page():
    return Clubs.objects.first().page
