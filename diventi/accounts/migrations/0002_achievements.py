# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-24 18:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=30, verbose_name='icon')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('color', models.CharField(choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='default', max_length=30, verbose_name='color')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Achievement',
                'verbose_name_plural': 'Achievements',
            },
        ),
    ]
