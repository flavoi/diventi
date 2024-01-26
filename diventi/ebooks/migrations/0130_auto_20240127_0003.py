# Generated by Django 2.2.28 on 2024-01-26 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0129_auto_20240102_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='part',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='replacementrule',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='secret',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='section',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='sectionaspect',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='universalsection',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
    ]
