# Generated by Django 2.2.28 on 2022-10-18 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_auto_20221018_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='courtesy_message_en',
            field=models.TextField(help_text='Folded products return this message to all users', null=True, verbose_name='courtesy message'),
        ),
        migrations.AddField(
            model_name='package',
            name='courtesy_message_it',
            field=models.TextField(help_text='Folded products return this message to all users', null=True, verbose_name='courtesy message'),
        ),
        migrations.AddField(
            model_name='package',
            name='courtesy_short_message_en',
            field=models.CharField(max_length=50, null=True, verbose_name='short courtesy messages'),
        ),
        migrations.AddField(
            model_name='package',
            name='courtesy_short_message_it',
            field=models.CharField(max_length=50, null=True, verbose_name='short courtesy messages'),
        ),
    ]
