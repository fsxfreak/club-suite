# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 08:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suite', '0024_auto_20170303_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='requests',
            field=models.ManyToManyField(related_name='JoinRequest', through='suite.JoinRequest', to=settings.AUTH_USER_MODEL),
        ),
    ]