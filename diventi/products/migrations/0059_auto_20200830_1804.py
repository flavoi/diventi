# Generated by Django 2.2.13 on 2020-08-30 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0058_auto_20200830_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
        migrations.AlterField(
            model_name='imagepreview',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
        migrations.AlterField(
            model_name='product',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
        migrations.AlterField(
            model_name='productformat',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
    ]
