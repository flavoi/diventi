# Generated by Django 2.1.7 on 2019-04-09 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0041_auto_20190402_0822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=30, verbose_name='icon')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('description_it', models.TextField(null=True, verbose_name='description')),
                ('description_en', models.TextField(null=True, verbose_name='description')),
                ('color', models.CharField(choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='default', max_length=30, verbose_name='color')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
            },
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='featured_link_en',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='featured_link_it',
        ),
        migrations.AddField(
            model_name='section',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sections', to='landing.Presentation'),
        ),
        migrations.AddField(
            model_name='feature',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='features', to='landing.Section'),
        ),
    ]
