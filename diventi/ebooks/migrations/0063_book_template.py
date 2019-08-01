# Generated by Django 2.2.3 on 2019-08-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0062_auto_20190619_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='template',
            field=models.CharField(choices=[('book_detail.html', 'Standard'), ('wbook_detail.html', 'Alternative')], default='book_detail.html', max_length=50, verbose_name='template'),
        ),
    ]
