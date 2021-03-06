# Generated by Django 2.0.5 on 2018-08-13 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0020_auto_20180805_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('abstract', models.TextField(blank=True, verbose_name='abstract')),
                ('abstract_it', models.TextField(blank=True, null=True, verbose_name='abstract')),
                ('abstract_en', models.TextField(blank=True, null=True, verbose_name='abstract')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_it', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'about',
                'verbose_name_plural': 'about',
            },
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='about',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='about_en',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='about_it',
        ),
        migrations.AddField(
            model_name='about',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='about', to='landing.Presentation'),
        ),
        migrations.AddField(
            model_name='feature',
            name='about',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='features', to='landing.About'),
        ),
    ]
