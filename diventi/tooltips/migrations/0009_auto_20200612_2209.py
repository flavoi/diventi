# Generated by Django 2.2.13 on 2020-06-12 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tooltips', '0008_auto_20200612_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tooltip',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tooltips', to='products.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='tooltip',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tooltips', to='ebooks.Section', verbose_name='section'),
        ),
    ]
