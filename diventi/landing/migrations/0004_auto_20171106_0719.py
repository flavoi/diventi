# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 07:19
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_auto_20171104_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='feature',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
