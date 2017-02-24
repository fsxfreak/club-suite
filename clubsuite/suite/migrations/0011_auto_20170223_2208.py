# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suite', '0010_merge_20170222_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
