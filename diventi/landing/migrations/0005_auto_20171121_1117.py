# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_auto_20171106_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='feature',
            name='description',
            field=models.TextField(),
        ),
    ]
