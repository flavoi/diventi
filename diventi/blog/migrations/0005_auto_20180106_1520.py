# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-06 14:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180106_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
    ]