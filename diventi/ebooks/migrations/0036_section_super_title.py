# Generated by Django 2.2.1 on 2019-05-24 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0035_section_text_alignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='super_title',
            field=models.BooleanField(default=False, verbose_name='super title'),
        ),
    ]
