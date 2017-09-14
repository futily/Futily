# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 18:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0010_player_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='rating_futily',
            field=models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AddField(
            model_name='player',
            name='rating_pirlo',
            field=models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AddField(
            model_name='player',
            name='rating_vidic',
            field=models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
    ]
