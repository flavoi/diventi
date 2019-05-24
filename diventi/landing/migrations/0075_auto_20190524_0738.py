# Generated by Django 2.2.1 on 2019-05-24 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0074_remove_section_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='icon',
            field=models.CharField(blank=True, max_length=30, verbose_name='icon'),
        ),
    ]
