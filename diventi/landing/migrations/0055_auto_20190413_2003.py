# Generated by Django 2.1.7 on 2019-04-13 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0054_auto_20190412_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='template',
            field=models.CharField(choices=[('standard_centered_section.html', 'standard centered section')], max_length=50, verbose_name='standard template'),
        ),
    ]
