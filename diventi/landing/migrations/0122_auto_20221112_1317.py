# Generated by Django 2.2.28 on 2022-11-12 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0121_auto_20221112_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='subtitle',
            field=models.CharField(blank=True, max_length=50, verbose_name='subtitle'),
        ),
        migrations.AddField(
            model_name='section',
            name='subtitle_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='subtitle'),
        ),
        migrations.AddField(
            model_name='section',
            name='subtitle_it',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='subtitle'),
        ),
    ]