# Generated by Django 2.2.28 on 2022-10-21 10:37

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_auto_20221021_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='package',
            name='description_en',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='package',
            name='description_it',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='description'),
        ),
    ]
