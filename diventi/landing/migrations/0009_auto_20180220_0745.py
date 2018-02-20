# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-20 06:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0008_remove_featurescover_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentationCover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(verbose_name='image')),
                ('label', models.CharField(blank=True, max_length=50, verbose_name='label')),
                ('label_it', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
                ('label_en', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
                ('section', models.CharField(choices=[('DES', 'description'), ('FEA', 'features')], default='DES', max_length=3)),
                ('default', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Presentation Cover',
                'verbose_name_plural': 'Presentation Covers',
            },
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='features_cover',
        ),
        migrations.DeleteModel(
            name='FeaturesCover',
        ),
        migrations.AddField(
            model_name='presentation',
            name='presentation_covers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='landing.PresentationCover', verbose_name='presentation cover'),
        ),
    ]
