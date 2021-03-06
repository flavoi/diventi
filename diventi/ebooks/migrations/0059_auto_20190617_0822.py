# Generated by Django 2.2.2 on 2019-06-17 06:22

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0058_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='content_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='content'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='content_it',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='content'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='title_it',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
    ]
