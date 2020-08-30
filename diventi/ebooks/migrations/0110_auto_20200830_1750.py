# Generated by Django 2.2.13 on 2020-08-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0109_auto_20200821_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='part',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='replacementrule',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='section',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='sectionaspect',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='universalsection',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color'),
        ),
    ]
