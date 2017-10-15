from django_jinja import library

from futily.apps.nations.models import Nations


@library.global_function
def get_nations_page():
    return Nations.objects.first().page
