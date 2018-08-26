# Generated by Django 2.0.8 on 2018-08-25 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0023_remove_paper_titlepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='section_type',
            field=models.CharField(blank=True, choices=[('section', 'section'), ('subsection', 'subsection'), ('commentbox', 'commentbox'), ('quotebox', 'quotebox'), ('paperbox', 'paperbox'), ('dicetable', 'dicetable'), ('titlepage', 'titlepage')], max_length=30, verbose_name='section type'),
        ),
        migrations.AlterField(
            model_name='watermark',
            name='scale',
            field=models.FloatField(default=1),
        ),
    ]