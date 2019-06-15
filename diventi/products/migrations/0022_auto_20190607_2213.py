# Generated by Django 2.2.1 on 2019-06-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20190607_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='courtesy_message',
            field=models.TextField(verbose_name='courtesy message'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_message_en',
            field=models.TextField(null=True, verbose_name='courtesy message'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_message_it',
            field=models.TextField(null=True, verbose_name='courtesy message'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_short_message',
            field=models.CharField(max_length=50, verbose_name='short courtesy messages'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_short_message_en',
            field=models.CharField(max_length=50, null=True, verbose_name='short courtesy messages'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_short_message_it',
            field=models.CharField(max_length=50, null=True, verbose_name='short courtesy messages'),
        ),
    ]