# Generated by Django 2.1.7 on 2019-04-30 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190430_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishablemodel',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
