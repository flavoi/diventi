# Generated by Django 2.1.7 on 2019-04-30 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0011_book_short_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(blank=True, max_length=100, verbose_name='category'),
        ),
    ]
