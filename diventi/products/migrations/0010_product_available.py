# Generated by Django 2.0.5 on 2018-08-11 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20180526_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=False, verbose_name='available'),
        ),
    ]
