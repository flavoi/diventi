# Generated by Django 2.1.7 on 2019-04-11 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0048_auto_20190411_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='template',
            field=models.CharField(choices=[('', '')], default='', max_length=50, verbose_name='template'),
            preserve_default=False,
        ),
    ]
