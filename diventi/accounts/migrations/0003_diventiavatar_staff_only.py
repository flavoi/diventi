# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171023_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='diventiavatar',
            name='staff_only',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
