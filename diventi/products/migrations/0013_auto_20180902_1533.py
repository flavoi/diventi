# Generated by Django 2.0.8 on 2018-09-02 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20180811_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagepreview',
            name='image_en',
            field=models.URLField(null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='imagepreview',
            name='image_it',
            field=models.URLField(null=True, verbose_name='image'),
        ),
    ]
