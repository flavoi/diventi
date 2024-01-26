# Generated by Django 2.2.28 on 2024-01-26 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0093_auto_20240126_2354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chaptercategory',
            name='default',
        ),
        migrations.AddField(
            model_name='chapter',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='chaptercategory',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Light blue'), ('primary', 'Blue'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('secondary', 'Light gray'), ('gray', 'Gray'), ('gray-dark', 'Black'), ('white', 'White'), ('indigo', 'Indigo'), ('purple', 'Purple'), ('pink', 'Pink'), ('cyan', 'Cyan')], default='default', max_length=30, verbose_name='color'),
        ),
        migrations.AddField(
            model_name='chaptercategory',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='chaptercategory',
            name='icon',
            field=models.CharField(blank=True, max_length=30, verbose_name='icon'),
        ),
        migrations.AddField(
            model_name='chaptercategory',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
        migrations.AddField(
            model_name='imagepreview',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='product',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='productcover',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AddField(
            model_name='productformat',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
        migrations.AlterField(
            model_name='chaptercategory',
            name='title',
            field=models.CharField(max_length=80, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='chaptercategory',
            name='title_en',
            field=models.CharField(max_length=80, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='chaptercategory',
            name='title_it',
            field=models.CharField(max_length=80, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='chaptercategory',
            name='title_plural',
            field=models.CharField(blank=True, max_length=80, verbose_name='plural title'),
        ),
    ]
