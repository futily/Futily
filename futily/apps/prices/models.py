from django.db import models


class Price(models.Model):
    market = models.CharField(max_length=255, choices=[
        ('pc', 'PC'),
        ('ps', 'Playstation'),
        ('xb', 'Xbox'),
    ])
    player = models.ForeignKey('players.Player')
    value = models.IntegerField()
    source = models.CharField(max_length=255, choices=[
        ('futbin', 'Futbin'),
        ('futhead', 'Futhead'),
        ('futwiz', 'Futwiz'),
    ])
    last_update = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'<{self.player}> {self.market}: {self.value}'
