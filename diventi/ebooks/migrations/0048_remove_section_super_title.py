# Generated by Django 2.2.1 on 2019-06-05 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0047_auto_20190605_0743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='super_title',
        ),
    ]