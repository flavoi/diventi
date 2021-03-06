# Generated by Django 2.1.7 on 2019-04-21 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0066_section_section_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='featured_template',
            field=models.CharField(choices=[('header_left.html', 'standard left header'), ('header_centered.html', 'standard centered header')], max_length=50, verbose_name='featured template'),
        ),
        migrations.AlterField(
            model_name='section',
            name='template',
            field=models.CharField(choices=[('section_centered.html', 'standard centered section')], max_length=50, verbose_name='standard template'),
        ),
    ]
