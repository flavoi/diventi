# Generated by Django 2.2.13 on 2020-06-10 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0042_auto_20200502_1924'),
        ('ebooks', '0106_auto_20200524_1227'),
        ('tooltips', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tooltip',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='tooltip',
            name='description_it',
        ),
        migrations.AddField(
            model_name='tooltip',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tooltip', to='products.Product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='tooltip',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebooks.Section', verbose_name='section'),
        ),
    ]
