# Generated by Django 2.2.1 on 2019-05-18 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0028_auto_20190518_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='internal_order_index',
        ),
    ]
