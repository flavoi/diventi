# Generated by Django 2.1.7 on 2019-04-15 06:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0058_auto_20190415_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='product_features', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='user_features', to=settings.AUTH_USER_MODEL),
        ),
    ]