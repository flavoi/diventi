# Generated by Django 2.1.7 on 2019-04-30 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0009_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='chapter_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebooks.Book', verbose_name='book'),
        ),
    ]