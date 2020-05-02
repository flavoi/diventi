# Generated by Django 2.2.12 on 2020-05-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0006_auto_20200502_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='antagonist',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='antagonist',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='antagonist',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='antagonist',
            name='title_it',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='antagonistgoal',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='antagonistgoal',
            name='description_it',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='antagonistgoal',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='antagonistgoal',
            name='title_it',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
    ]
