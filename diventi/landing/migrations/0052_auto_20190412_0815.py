# Generated by Django 2.1.7 on 2019-04-12 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0051_auto_20190411_0812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='profile',
            new_name='presentation',
        ),
    ]
