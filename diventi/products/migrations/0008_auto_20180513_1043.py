# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-13 08:43
from __future__ import unicode_literals

import diventi.core.storages
import diventi.products.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20180319_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='file_en',
            field=diventi.products.fields.ProtectedFileField(blank=True, null=True, storage=diventi.core.storages.MediaStorage(acl='private'), upload_to='products/files/', verbose_name='file'),
        ),
        migrations.AddField(
            model_name='product',
            name='file_it',
            field=diventi.products.fields.ProtectedFileField(blank=True, null=True, storage=diventi.core.storages.MediaStorage(acl='private'), upload_to='products/files/', verbose_name='file'),
        ),
    ]
