# Generated by Django 2.0.8 on 2019-03-23 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0031_remove_presentation_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='primary_link',
            field=models.URLField(blank=True, verbose_name='primary link'),
        ),
    ]