# Generated by Django 2.2.13 on 2020-08-26 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0094_auto_20200821_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='position',
            field=models.PositiveIntegerField(choices=[(1, 'text first'), (3, 'text second')], default=1, verbose_name='text position'),
        ),
    ]
