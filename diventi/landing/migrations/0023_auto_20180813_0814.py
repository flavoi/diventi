# Generated by Django 2.0.5 on 2018-08-13 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0022_remove_feature_about'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='abstract',
        ),
        migrations.RemoveField(
            model_name='about',
            name='abstract_en',
        ),
        migrations.RemoveField(
            model_name='about',
            name='abstract_it',
        ),
    ]
