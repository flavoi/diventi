# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-09 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20171209_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='image',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chapter',
            name='label',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]