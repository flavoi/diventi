# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-24 12:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20180523_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diventiuser',
            name='has_agreed_gdpr',
        ),
        migrations.RemoveField(
            model_name='diventiuser',
            name='language',
        ),
    ]