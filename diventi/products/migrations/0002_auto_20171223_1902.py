# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-23 18:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='buyers',
            field=models.ManyToManyField(blank=True, null=True, related_name='collection', to=settings.AUTH_USER_MODEL),
        ),
    ]