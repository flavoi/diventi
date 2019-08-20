# Generated by Django 2.2.4 on 2019-08-20 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0076_section_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.URLField(blank=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='book',
            name='label',
            field=models.CharField(blank=True, max_length=50, verbose_name='label'),
        ),
    ]
