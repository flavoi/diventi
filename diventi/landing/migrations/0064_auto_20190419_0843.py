# Generated by Django 2.1.7 on 2019-04-19 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0063_auto_20190419_0821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='_survey',
            new_name='section_survey',
        ),
    ]
