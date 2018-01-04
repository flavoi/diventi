# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiventiCover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField()),
                ('label', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Cover',
                'verbose_name_plural': 'Covers',
            },
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.DiventiCover'),
        ),
    ]
