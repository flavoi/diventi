# Generated by Django 2.2.13 on 2020-08-27 13:04

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190430_1532'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landing', '0095_auto_20200826_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutArticle',
            fields=[
                ('publishablemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.PublishableModel')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('icon', models.CharField(blank=True, max_length=30, verbose_name='icon')),
                ('icon_style', models.CharField(choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color')),
                ('content', ckeditor.fields.RichTextField(verbose_name='content')),
                ('content_it', ckeditor.fields.RichTextField(null=True, verbose_name='content')),
                ('content_en', ckeditor.fields.RichTextField(null=True, verbose_name='content')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('slug_it', models.SlugField(null=True, unique=True, verbose_name='slug')),
                ('slug_en', models.SlugField(null=True, unique=True, verbose_name='slug')),
                ('promotions', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='promotions')),
            ],
            options={
                'verbose_name': 'about article',
                'verbose_name_plural': 'about article',
            },
            bases=('core.publishablemodel', models.Model),
        ),
    ]