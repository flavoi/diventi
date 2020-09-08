# Generated by Django 2.2.13 on 2020-08-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tooltips', '0011_auto_20200830_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tooltip',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
        migrations.AlterField(
            model_name='tooltipgroup',
            name='icon_style',
            field=models.CharField(blank=True, choices=[('r', 'r - regular'), ('s', 's - solid'), ('l', 'l - light'), ('d', 'd - duotone'), ('b', 'b - brand')], default='r', max_length=1, verbose_name='icon style'),
        ),
    ]