# Generated by Django 2.0.8 on 2018-10-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0002_auto_20181007_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author_name',
            field=models.CharField(max_length=60, verbose_name='author name'),
        ),
    ]
