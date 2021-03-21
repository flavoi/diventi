# Generated by Django 2.2.16 on 2021-03-21 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_article_col_sm'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='order_lg',
            field=models.PositiveIntegerField(default=1, verbose_name='lg order'),
        ),
        migrations.AddField(
            model_name='article',
            name='order_md',
            field=models.PositiveIntegerField(default=1, verbose_name='md order'),
        ),
        migrations.AddField(
            model_name='article',
            name='order_sm',
            field=models.PositiveIntegerField(default=1, verbose_name='sm order'),
        ),
    ]
