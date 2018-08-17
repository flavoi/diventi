# Generated by Django 2.1 on 2018-08-17 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brew',
            name='content_en',
            field=models.TextField(null=True, verbose_name='content'),
        ),
        migrations.AddField(
            model_name='brew',
            name='content_it',
            field=models.TextField(null=True, verbose_name='content'),
        ),
        migrations.AddField(
            model_name='brew',
            name='description_en',
            field=models.TextField(max_length=250, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='brew',
            name='description_it',
            field=models.TextField(max_length=250, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='brew',
            name='slug_en',
            field=models.SlugField(null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='brew',
            name='slug_it',
            field=models.SlugField(null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='brew',
            name='title_en',
            field=models.CharField(max_length=60, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='brew',
            name='title_it',
            field=models.CharField(max_length=60, null=True, verbose_name='title'),
        ),
    ]