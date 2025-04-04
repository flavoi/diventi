# Generated by Django 2.2.28 on 2025-04-04 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0139_book_paper_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='legacy_paper_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='legacy paper id'),
        ),
        migrations.AlterField(
            model_name='book',
            name='legacy_paper_id_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='legacy paper id'),
        ),
        migrations.AlterField(
            model_name='book',
            name='legacy_paper_id_it',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='legacy paper id'),
        ),
    ]
