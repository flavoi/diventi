# Generated by Django 2.2.28 on 2025-01-19 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0127_auto_20240127_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(blank=True, verbose_name='image')),
                ('label', models.CharField(blank=True, max_length=50, verbose_name='label')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
