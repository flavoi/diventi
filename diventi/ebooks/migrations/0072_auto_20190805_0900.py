# Generated by Django 2.2.3 on 2019-08-05 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0071_auto_20190805_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='template',
            field=models.CharField(choices=[('material', 'Material'), ('web', 'Web')], default='material', max_length=50, verbose_name='template'),
        ),
    ]
