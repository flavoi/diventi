# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 11:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_auto_20171009_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentation',
            name='paper_url',
        ),
    ]