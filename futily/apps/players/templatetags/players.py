from django_jinja import library


@library.global_function
def stat_grade(val):
    if val >= 81:
        return 'great'
    elif 80 <= val >= 71:
        return 'good'
    elif 70 <= val >= 61:
        return 'average'
    elif 60 <= val >= 51:
        return 'fair'

    return 'poor'
