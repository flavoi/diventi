# Generated by Django 2.2.24 on 2021-09-30 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0106_auto_20210930_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='articles',
        ),
        migrations.RemoveField(
            model_name='section',
            name='dark_mode',
        ),
        migrations.RemoveField(
            model_name='section',
            name='featured_template',
        ),
        migrations.RemoveField(
            model_name='section',
            name='products',
        ),
        migrations.RemoveField(
            model_name='section',
            name='section_survey',
        ),
        migrations.RemoveField(
            model_name='section',
            name='template',
        ),
        migrations.RemoveField(
            model_name='section',
            name='users',
        ),
    ]