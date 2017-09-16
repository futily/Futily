from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.template.loader import render_to_string


class Action(models.Model):
    user = models.ForeignKey('users.User', related_name='actions', db_index=True)
    verb = models.CharField(max_length=255)

    extra = models.TextField(blank=True, null=True)
    target_ct = models.ForeignKey('contenttypes.ContentType', blank=True, null=True, related_name='target_obj')
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user} {self.verb} {self.target}'

    @property
    def html__str__(self):
        return render_to_string('actions/__str__.html', {
            'action': self
        })
