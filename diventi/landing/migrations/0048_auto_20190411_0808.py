# Generated by Django 2.1.7 on 2019-04-11 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0047_auto_20190411_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='color',
        ),
        migrations.RemoveField(
            model_name='section',
            name='icon',
        ),
        migrations.AddField(
            model_name='section',
            name='abstract',
            field=models.TextField(blank=True, verbose_name='abstract'),
        ),
        migrations.AlterField(
            model_name='section',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='section',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='section',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]
