# Generated by Django 2.1.7 on 2019-04-01 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0036_survey_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='public',
        ),
    ]
