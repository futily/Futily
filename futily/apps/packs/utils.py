from ..players.models import Player


def color_choices():
    colors = Player.objects.values_list('color', flat=True).order_by('color').distinct()

    if colors:
        return [
            (x, x.capitalize().replace('_', ' ')) for x in colors
        ]

    return [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]
