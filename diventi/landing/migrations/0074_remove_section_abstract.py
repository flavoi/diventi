# Generated by Django 2.1.7 on 2019-04-24 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0073_auto_20190423_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='abstract',
        ),
    ]
