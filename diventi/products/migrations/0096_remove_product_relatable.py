# Generated by Django 2.2.28 on 2024-01-28 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0095_auto_20240127_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='relatable',
        ),
    ]
