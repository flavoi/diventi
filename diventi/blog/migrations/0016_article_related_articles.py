# Generated by Django 2.2.13 on 2020-08-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20200718_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='related_articles',
            field=models.ManyToManyField(blank=True, related_name='_article_related_articles_+', to='blog.Article', verbose_name='related articles'),
        ),
    ]
