# Generated by Django 2.2.28 on 2025-04-04 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0137_book_continuous_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='paper_id',
            new_name='legacy_paper_id',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='paper_id_en',
            new_name='legacy_paper_id_en',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='paper_id_it',
            new_name='legacy_paper_id_it',
        ),
    ]
