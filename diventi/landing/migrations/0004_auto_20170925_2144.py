# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 21:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_auto_20170924_0850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presentation',
            old_name='staff_special_url',
            new_name='paper_url',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='staff_special_color',
        ),
    ]
