# Generated by Django 2.2.24 on 2022-01-23 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0075_product_hot'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='title')),
                ('title_it', models.CharField(max_length=80, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=80, null=True, verbose_name='title')),
                ('icon', models.CharField(blank=True, max_length=30, verbose_name='icon')),
                ('icon_style', models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_it', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('color', models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='default', max_length=30, verbose_name='color')),
                ('image', models.URLField(blank=True, verbose_name='image')),
                ('label', models.CharField(blank=True, max_length=50, verbose_name='label')),
                ('label_it', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
                ('label_en', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
            ],
            options={
                'verbose_name': 'Product Cover',
                'verbose_name_plural': 'Product Covers',
            },
        ),
    ]
