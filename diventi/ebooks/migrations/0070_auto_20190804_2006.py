# Generated by Django 2.2.3 on 2019-08-04 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0069_auto_20190804_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='template',
            field=models.CharField(choices=[('', 'Material'), ('web', 'Web')], default='', max_length=50, verbose_name='template'),
        ),
    ]
