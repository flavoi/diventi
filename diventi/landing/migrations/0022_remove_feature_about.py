# Generated by Django 2.0.5 on 2018-08-13 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0021_auto_20180813_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='about',
        ),
    ]
