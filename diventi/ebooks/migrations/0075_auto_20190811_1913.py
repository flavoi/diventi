# Generated by Django 2.2.4 on 2019-08-11 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0074_update_template_names'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='bookmark',
        ),
        migrations.RemoveField(
            model_name='section',
            name='card_type',
        ),
        migrations.RemoveField(
            model_name='section',
            name='template',
        ),
    ]
