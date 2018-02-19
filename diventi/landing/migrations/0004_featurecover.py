# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-17 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_auto_20180216_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureCover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(verbose_name='image')),
                ('label', models.CharField(blank=True, max_length=50, verbose_name='label')),
            ],
            options={
                'verbose_name': 'Feature Cover',
                'verbose_name_plural': 'Feature Covers',
            },
        ),
    ]