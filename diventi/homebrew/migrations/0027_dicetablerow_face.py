# Generated by Django 2.0.8 on 2018-08-25 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0026_auto_20180825_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicetablerow',
            name='face',
            field=models.PositiveIntegerField(default=1, verbose_name='face'),
            preserve_default=False,
        ),
    ]