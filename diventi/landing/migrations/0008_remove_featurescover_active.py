# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-17 20:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0007_auto_20180217_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featurescover',
            name='active',
        ),
    ]
