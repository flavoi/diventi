# Generated by Django 2.0.8 on 2018-10-04 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0051_section__card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='_card',
        ),
    ]