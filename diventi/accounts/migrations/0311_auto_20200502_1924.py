# Generated by Django 2.2.12 on 2020-05-02 17:24

import diventi.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0310_auto_20200502_1924'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='diventiuser',
            managers=[
                ('objects', diventi.accounts.models.DiventiUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='achievement',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='role',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
    ]
