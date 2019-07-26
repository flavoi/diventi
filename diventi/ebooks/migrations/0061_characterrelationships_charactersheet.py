# Generated by Django 2.2.2 on 2019-06-19 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0060_auto_20190618_0829'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('origin', models.CharField(max_length=50, verbose_name='origin')),
                ('predisposition', models.CharField(max_length=50, verbose_name='predisposition')),
            ],
            options={
                'verbose_name': 'character sheet',
                'verbose_name_plural': 'character sheets',
            },
        ),
        migrations.CreateModel(
            name='CharacterRelationships',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('icon', models.CharField(blank=True, max_length=30, verbose_name='icon')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='warning', max_length=30, verbose_name='color')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebooks.CharacterSheet', verbose_name='character')),
            ],
            options={
                'verbose_name': 'relationship',
                'verbose_name_plural': 'relationships',
            },
        ),
    ]