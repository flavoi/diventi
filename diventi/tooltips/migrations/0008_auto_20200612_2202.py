# Generated by Django 2.2.13 on 2020-06-12 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tooltips', '0007_auto_20200612_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tooltipgroup',
            name='books',
            field=models.ManyToManyField(blank=True, to='ebooks.Book', verbose_name='book'),
        ),
    ]
