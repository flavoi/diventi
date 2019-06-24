# Generated by Django 2.2.2 on 2019-06-20 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0002_auto_20190620_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charactersheet',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebooks.Book', verbose_name='book'),
        ),
        migrations.AlterField(
            model_name='charactersheet',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='player'),
        ),
    ]
