# Generated by Django 2.0.8 on 2019-02-01 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180520_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='diventiuser',
            name='bio_en',
            field=models.TextField(blank=True, null=True, verbose_name='bio'),
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='bio_it',
            field=models.TextField(blank=True, null=True, verbose_name='bio'),
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='has_agreed_gdpr',
            field=models.NullBooleanField(verbose_name='subscriber status'),
        ),
        migrations.AlterField(
            model_name='diventiuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
