# Generated by Django 2.2.10 on 2020-03-01 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0036_auto_20200301_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='alignment',
            field=models.CharField(choices=[('left', 'left'), ('centered', 'centered'), ('right', 'right')], default='left', max_length=50, verbose_name='alignment'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='product'),
        ),
    ]
