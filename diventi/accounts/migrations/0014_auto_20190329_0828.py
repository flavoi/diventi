# Generated by Django 2.1.7 on 2019-03-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190301_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diventiuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
