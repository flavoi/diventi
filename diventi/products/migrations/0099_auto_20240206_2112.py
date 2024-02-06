# Generated by Django 2.2.28 on 2024-02-06 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0098_auto_20240206_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='formats',
        ),
        migrations.AddField(
            model_name='product',
            name='formats',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.ProductFormat', verbose_name='formats'),
        ),
    ]
