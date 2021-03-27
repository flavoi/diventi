# Generated by Django 2.2.16 on 2021-03-21 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0064_product_pinned'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='col_lg',
            field=models.PositiveIntegerField(choices=[(12, 'Wide'), (8, 'Three fourths'), (6, 'Half'), (4, 'Narrow')], default=12, verbose_name='lg column'),
        ),
        migrations.AddField(
            model_name='product',
            name='col_md',
            field=models.PositiveIntegerField(choices=[(12, 'Wide'), (8, 'Three fourths'), (6, 'Half'), (4, 'Narrow')], default=12, verbose_name='md column'),
        ),
    ]