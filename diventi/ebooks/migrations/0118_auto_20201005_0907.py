# Generated by Django 2.2.16 on 2020-10-05 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0117_auto_20200924_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='logo',
            field=models.URLField(blank=True, verbose_name='logo'),
        ),
        migrations.AddField(
            model_name='book',
            name='logo_background',
            field=models.CharField(choices=[('secondary', 'Secondary'), ('primary', 'Primary'), ('dark', 'Dark')], default='secondary', max_length=30, verbose_name='logo background'),
        ),
    ]
