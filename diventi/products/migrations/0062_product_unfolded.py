# Generated by Django 2.2.16 on 2020-09-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0061_auto_20200902_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unfolded',
            field=models.BooleanField(default=False, verbose_name='unfolded'),
        ),
    ]