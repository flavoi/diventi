# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-04 19:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20180204_1833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chaptercategory',
            options={'verbose_name': 'Chapter category', 'verbose_name_plural': 'Chapter categories'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Product category', 'verbose_name_plural': 'Product categories'},
        ),
    ]
