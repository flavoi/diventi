# Generated by Django 2.2.28 on 2024-03-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0136_auto_20240227_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='continuous_update',
            field=models.BooleanField(default=False, verbose_name='continuous update'),
        ),
    ]
