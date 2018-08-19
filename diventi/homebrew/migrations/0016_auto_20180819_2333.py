# Generated by Django 2.0.8 on 2018-08-19 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0015_dicetablerow_dicetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicetable',
            name='dice',
            field=models.CharField(choices=[('20', 'd20'), ('12', 'd12'), ('10', 'd10'), ('8', 'd8'), ('6', 'd6'), ('4', 'd4')], max_length=3, verbose_name='dice'),
        ),
    ]
