# Generated by Django 2.1.7 on 2019-04-02 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0038_auto_20190329_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='featured_link_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='featured link'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='featured_link_it',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='featured link'),
        ),
    ]
