# Generated by Django 2.2.13 on 2020-08-28 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0096_aboutarticle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutarticle',
            name='promotions',
        ),
    ]
