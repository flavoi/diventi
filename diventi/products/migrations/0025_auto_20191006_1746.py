# Generated by Django 2.2.4 on 2019-10-06 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_auto_20190813_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='courtesy_message',
            field=models.TextField(blank=True, verbose_name='courtesy message'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_message_en',
            field=models.TextField(blank=True, null=True, verbose_name='courtesy message'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_message_it',
            field=models.TextField(blank=True, null=True, verbose_name='courtesy message'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_short_message',
            field=models.CharField(blank=True, max_length=50, verbose_name='short courtesy messages'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_short_message_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='short courtesy messages'),
        ),
        migrations.AlterField(
            model_name='product',
            name='courtesy_short_message_it',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='short courtesy messages'),
        ),
    ]
