# Generated by Django 2.0.8 on 2018-08-26 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0033_auto_20180826_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='content',
            field=models.TextField(blank=True, verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='section',
            name='content_en',
            field=models.TextField(blank=True, null=True, verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='section',
            name='content_it',
            field=models.TextField(blank=True, null=True, verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_type',
            field=models.CharField(blank=True, choices=[('section', 'section'), ('subsection', 'subsection'), ('paragraph', 'paragraph'), ('commentbox', 'commentbox'), ('quotebox', 'quotebox'), ('paperbox', 'paperbox'), ('header', 'header'), ('phantom', 'phantom')], max_length=30, verbose_name='section type'),
        ),
    ]
