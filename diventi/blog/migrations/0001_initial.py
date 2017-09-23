# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 08:16
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=60)),
                ('image', models.ImageField(blank=True, upload_to='articles/')),
                ('caption', models.CharField(blank=True, max_length=60)),
                ('content', ckeditor.fields.RichTextField()),
                ('published', models.BooleanField(default=False)),
                ('publication_date', models.DateField(auto_now_add=True, null=True)),
                ('hot', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('file', models.FileField(upload_to='media/attachments/')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
    ]
