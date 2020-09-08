# Generated by Django 2.2.13 on 2020-08-28 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0054_product_stripe_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='stripe_product',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='stripe product'),
        ),
    ]