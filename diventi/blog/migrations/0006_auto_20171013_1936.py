# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 19:36
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=ckeditor.fields.RichTextField(max_length=250),
        ),
    ]