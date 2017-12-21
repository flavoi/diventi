# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 21:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0011_auto_20171209_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='authors',
            field=models.ManyToManyField(related_name='products', to=settings.AUTH_USER_MODEL),
        ),
    ]
