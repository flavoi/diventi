# Generated by Django 2.2.24 on 2022-01-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0107_auto_20210930_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='button_label',
            field=models.CharField(default='', max_length=50, verbose_name='label'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='button_label_en',
            field=models.CharField(max_length=50, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='section',
            name='button_label_it',
            field=models.CharField(max_length=50, null=True, verbose_name='label'),
        ),
    ]
