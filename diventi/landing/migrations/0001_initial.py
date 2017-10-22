# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 08:50
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
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=50)),
                ('description', ckeditor.fields.RichTextField()),
                ('color', models.CharField(choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('success', 'Green'), ('default', 'Gray')], default='default', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('abstract', ckeditor.fields.RichTextField(blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='landing/')),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='feature',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.Presentation'),
        ),
    ]
