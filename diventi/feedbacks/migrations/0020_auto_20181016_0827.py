# Generated by Django 2.0.8 on 2018-10-16 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0019_auto_20181016_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='image',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='label',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='label_en',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='label_it',
        ),
    ]
