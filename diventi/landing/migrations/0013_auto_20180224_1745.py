# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-24 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0012_auto_20180220_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentation',
            name='presentation_covers',
        ),
        migrations.AddField(
            model_name='presentation',
            name='presentation_covers',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='landing.PresentationCover', verbose_name='presentation covers'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='presentationcover',
            name='section',
            field=models.CharField(choices=[('DES', 'description'), ('FEA', 'features'), ('PRO', 'products')], default='DES', max_length=3, verbose_name='section'),
        ),
    ]
