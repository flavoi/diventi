# Generated by Django 2.1.7 on 2019-04-12 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0052_auto_20190412_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
            preserve_default=False,
        ),
    ]
