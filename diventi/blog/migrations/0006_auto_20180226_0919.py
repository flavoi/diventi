# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-26 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180212_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='article',
            name='caption_en',
        ),
        migrations.RemoveField(
            model_name='article',
            name='caption_it',
        ),
        migrations.AddField(
            model_name='article',
            name='label',
            field=models.CharField(blank=True, max_length=50, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='article',
            name='label_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='article',
            name='label_it',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.URLField(verbose_name='image'),
        ),
    ]