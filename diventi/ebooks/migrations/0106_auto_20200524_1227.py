# Generated by Django 2.2.12 on 2020-05-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0105_auto_20200517_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='new',
            field=models.BooleanField(default=False, verbose_name='new'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='updated',
            field=models.BooleanField(default=False, verbose_name='updated'),
        ),
    ]