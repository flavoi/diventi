# Generated by Django 2.1.7 on 2019-05-03 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0014_book_book_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
    ]