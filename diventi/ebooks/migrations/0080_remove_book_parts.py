# Generated by Django 2.2.4 on 2019-10-06 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0079_auto_20191006_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='parts',
        ),
    ]