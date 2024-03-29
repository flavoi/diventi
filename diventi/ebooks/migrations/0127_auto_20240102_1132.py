# Generated by Django 2.2.28 on 2024-01-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0126_auto_20210321_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='part',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='replacementrule',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='section',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='sectionaspect',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='universalsection',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('gray', 'Light gray')], default='default', max_length=30, verbose_name='color'),
        ),
    ]
