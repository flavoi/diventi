# Generated by Django 2.1.7 on 2019-04-11 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20190120_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='image',
            field=models.URLField(blank=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='imagepreview',
            name='image',
            field=models.URLField(blank=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='imagepreview',
            name='image_en',
            field=models.URLField(blank=True, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='imagepreview',
            name='image_it',
            field=models.URLField(blank=True, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, verbose_name='image'),
        ),
    ]
