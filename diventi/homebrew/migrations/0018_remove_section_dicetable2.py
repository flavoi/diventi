# Generated by Django 2.0.8 on 2018-08-19 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0017_section_dicetable2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='dicetable2',
        ),
    ]