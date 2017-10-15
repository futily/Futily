from django_jinja import library

from futily.apps.players.models import Players


@library.global_function
def get_players_page():
    return Players.objects.first().page


@library.global_function
def stat_grade(val):
    if val >= 81:
        return 'great'
    elif val >= 71:
        return 'good'
    elif val >= 61:
        return 'average'
    elif val >= 51:
        return 'fair'

    return 'poor'
