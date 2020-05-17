# Generated by Django 2.2.12 on 2020-05-17 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200502_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='col_lg',
            field=models.PositiveIntegerField(choices=[(12, 'Wide'), (6, 'Half'), (4, 'Narrow')], default=12, verbose_name='lg column'),
        ),
        migrations.AddField(
            model_name='article',
            name='col_md',
            field=models.PositiveIntegerField(choices=[(12, 'Wide'), (6, 'Half'), (4, 'Narrow')], default=12, verbose_name='md column'),
        ),
    ]
