# Generated by Django 2.2.3 on 2019-08-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0068_auto_20190804_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='lead',
            field=models.TextField(blank=True, verbose_name='lead'),
        ),
        migrations.AlterField(
            model_name='book',
            name='lead_en',
            field=models.TextField(blank=True, null=True, verbose_name='lead'),
        ),
        migrations.AlterField(
            model_name='book',
            name='lead_it',
            field=models.TextField(blank=True, null=True, verbose_name='lead'),
        ),
    ]