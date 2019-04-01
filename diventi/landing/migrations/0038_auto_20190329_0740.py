# Generated by Django 2.0.13 on 2019-03-29 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0037_presentation_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='template',
            field=models.CharField(choices=[('standard_left_header.html', 'standard left header'), ('survey_centered_header.html', 'survey centered header')], max_length=50, verbose_name='template'),
        ),
    ]