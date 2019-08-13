# Generated by Django 2.2.4 on 2019-08-13 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_product_related_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, related_name='_product_related_products_+', to='products.Product', verbose_name='related products'),
        ),
    ]
