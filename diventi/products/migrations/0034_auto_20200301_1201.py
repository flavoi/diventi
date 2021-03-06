# Generated by Django 2.2.10 on 2020-03-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_productdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetail',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='title_it',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
    ]
