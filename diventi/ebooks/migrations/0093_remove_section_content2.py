# Generated by Django 2.2.10 on 2020-03-15 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0092_auto_20200315_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='content2',
        ),
    ]
