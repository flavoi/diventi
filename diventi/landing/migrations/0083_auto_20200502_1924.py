# Generated by Django 2.2.12 on 2020-05-02 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0082_auto_20200302_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='color',
            field=models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray'), ('dark', 'Black'), ('light', 'White')], default='warning', max_length=30, verbose_name='color'),
        ),
    ]
