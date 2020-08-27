# Generated by Django 2.2.13 on 2020-06-12 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0106_auto_20200524_1227'),
        ('tooltips', '0006_auto_20200612_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tooltip',
            name='books',
        ),
        migrations.AddField(
            model_name='tooltipgroup',
            name='books',
            field=models.ManyToManyField(to='ebooks.Book', verbose_name='book'),
        ),
    ]