# Generated by Django 2.0.8 on 2018-08-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0038_auto_20180830_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='illustration',
            field=models.CharField(blank=True, choices=[('parassite', 'parassite')], max_length=30, verbose_name='illustration'),
        ),
    ]
