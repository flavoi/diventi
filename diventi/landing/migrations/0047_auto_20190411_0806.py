# Generated by Django 2.1.7 on 2019-04-11 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0046_auto_20190411_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='image',
            field=models.URLField(blank=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='section',
            name='image',
            field=models.URLField(blank=True, verbose_name='image'),
        ),
    ]
