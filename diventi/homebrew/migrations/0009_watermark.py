# Generated by Django 2.0.8 on 2018-08-19 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0008_auto_20180819_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watermark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=60, verbose_name='title')),
                ('title_it', models.CharField(max_length=60, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=60, null=True, verbose_name='title')),
                ('pages', models.CharField(max_length=10, verbose_name='pages')),
                ('scale', models.PositiveIntegerField(default=1)),
                ('xpos', models.IntegerField()),
                ('ypos', models.IntegerField()),
                ('figurename', models.CharField(max_length=60, verbose_name='figure name')),
                ('paper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='watermarks', to='homebrew.Paper')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]