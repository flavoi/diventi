# Generated by Django 2.0.8 on 2018-08-30 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0040_auto_20180830_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='_illustration',
            field=models.CharField(blank=True, choices=[('parassite', 'parassite')], max_length=30, verbose_name='illustration'),
        ),
    ]