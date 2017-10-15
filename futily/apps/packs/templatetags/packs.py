from django_jinja import library

from futily.apps.packs.models import Packs


@library.global_function
def get_packs_page():
    return Packs.objects.first().page
