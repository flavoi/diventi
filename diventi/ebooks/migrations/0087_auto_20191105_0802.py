# Generated by Django 2.2.4 on 2019-11-05 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0086_auto_20191023_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='rules',
            field=models.ManyToManyField(blank=True, to='ebooks.ReplacementRule', verbose_name='rules'),
        ),
    ]
