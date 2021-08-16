# Generated by Django 2.2.24 on 2021-08-16 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0104_section_prefix'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='prefix_en',
            field=models.TextField(blank=True, null=True, verbose_name='prefix text'),
        ),
        migrations.AddField(
            model_name='section',
            name='prefix_it',
            field=models.TextField(blank=True, null=True, verbose_name='prefix text'),
        ),
    ]
