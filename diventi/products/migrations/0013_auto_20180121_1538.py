# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-21 14:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_en',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category', verbose_name='category'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_it',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category', verbose_name='category'),
        ),
    ]
