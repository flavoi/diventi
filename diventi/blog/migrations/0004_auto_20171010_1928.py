# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20171009_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='promotions',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
