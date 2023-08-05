# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 21:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orchestra', '0036_remove_taskassignment_snapshots'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteration',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='iteration',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
