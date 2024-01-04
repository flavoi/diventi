# Generated by Django 2.2.28 on 2024-01-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0089_auto_20230317_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='imagepreview',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='productcover',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='productformat',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
    ]