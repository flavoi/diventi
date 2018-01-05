# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-04 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_auto_20180103_1604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentation',
            options={'verbose_name': 'presentation', 'verbose_name_plural': 'presentations'},
        ),
        migrations.AlterField(
            model_name='presentation',
            name='active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
    ]
