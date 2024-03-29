# Generated by Django 2.2.24 on 2022-01-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0108_auto_20220121_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='button_label',
            field=models.CharField(blank=True, max_length=50, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='section',
            name='button_label_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='section',
            name='button_label_it',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='label'),
        ),
    ]
