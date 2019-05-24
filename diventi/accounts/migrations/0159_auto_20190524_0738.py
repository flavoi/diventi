# Generated by Django 2.2.1 on 2019-05-24 05:38

import diventi.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0158_auto_20190524_0731'),
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
            field=models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='icon',
            field=models.CharField(blank=True, max_length=30, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='role',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='role',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='role',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='role',
            name='icon',
            field=models.CharField(blank=True, max_length=30, verbose_name='icon'),
        ),
    ]
