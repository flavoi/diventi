# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-04 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diventiuser',
            name='landing_page_visibility',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
