# Generated by Django 2.2.13 on 2020-07-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0085_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='story',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='story',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='story',
            name='title_it',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
    ]
