# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-01 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20180101_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='diventicomment',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]