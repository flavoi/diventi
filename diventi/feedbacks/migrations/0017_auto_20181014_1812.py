# Generated by Django 2.0.8 on 2018-10-14 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0016_auto_20181014_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='survey',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]
