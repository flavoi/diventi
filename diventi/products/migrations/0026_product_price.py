# Generated by Django 2.2.4 on 2019-11-05 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20191006_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='price'),
            preserve_default=False,
        ),
    ]
