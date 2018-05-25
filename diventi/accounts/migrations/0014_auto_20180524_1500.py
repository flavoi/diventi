# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-24 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20180524_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='diventiuser',
            name='has_agreed_gdpr',
            field=models.BooleanField(default=False, verbose_name='has agreed to gdpr'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='language',
            field=models.CharField(blank=True, choices=[('it', 'Italian'), ('en', 'English')], default='en', max_length=2, verbose_name='language'),
        ),
    ]
