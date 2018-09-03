# Generated by Django 2.0.8 on 2018-09-03 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0023_auto_20180813_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutCover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(verbose_name='image')),
                ('label', models.CharField(blank=True, max_length=50, verbose_name='label')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
            ],
            options={
                'verbose_name': 'About Cover',
                'verbose_name_plural': 'About Covers',
            },
        ),
    ]
