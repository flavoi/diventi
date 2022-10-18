# Generated by Django 2.2.28 on 2022-10-16 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0079_auto_20221016_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='pinned',
            field=models.BooleanField(default=False, help_text='Pinned packages appear on the landing page', verbose_name='pinned'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pinned',
            field=models.BooleanField(default=False, help_text='Pinned products appear on the landing page', verbose_name='pinned'),
        ),
    ]
