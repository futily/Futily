# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-18 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flycomment',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
