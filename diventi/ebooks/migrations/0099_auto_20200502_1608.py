# Generated by Django 2.2.12 on 2020-05-02 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0098_secret'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sectionaspect',
            old_name='secction',
            new_name='section',
        ),
    ]