# Generated by Django 2.2.16 on 2020-09-02 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0060_auto_20200901_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, max_length=50, verbose_name='short description'),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description_en',
            field=models.TextField(blank=True, max_length=50, null=True, verbose_name='short description'),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description_it',
            field=models.TextField(blank=True, max_length=50, null=True, verbose_name='short description'),
        ),
    ]
