# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-01 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbc', '0005_squadbuilderchallengeset_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='squadbuilderchallenge',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
