# Generated by Django 2.0.5 on 2018-08-05 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0019_presentation_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='about_en',
            field=models.TextField(blank=True, null=True, verbose_name='about'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='about_it',
            field=models.TextField(blank=True, null=True, verbose_name='about'),
        ),
    ]
