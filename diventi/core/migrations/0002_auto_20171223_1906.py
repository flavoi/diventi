# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-23 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishablemodel',
            name='publication_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
