# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-28 11:27
from __future__ import unicode_literals

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiventiUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('profilepic', models.ImageField(blank=True, upload_to='accounts/profilepics/', verbose_name='profilepic')),
                ('bio', models.TextField(blank=True, verbose_name='bio')),
                ('role', models.CharField(blank=True, max_length=70, verbose_name='role')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='DiventiAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(verbose_name='image')),
                ('label', models.CharField(blank=True, max_length=50, verbose_name='label')),
                ('label_it', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
                ('label_en', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
                ('staff_only', models.BooleanField(default=False, verbose_name='staff_only')),
            ],
            options={
                'verbose_name': 'Avatar',
                'verbose_name_plural': 'Avatars',
            },
        ),
        migrations.CreateModel(
            name='DiventiCover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(verbose_name='image')),
                ('label', models.CharField(blank=True, max_length=50, verbose_name='label')),
                ('label_it', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
                ('label_en', models.CharField(blank=True, max_length=50, null=True, verbose_name='label')),
            ],
            options={
                'verbose_name': 'Cover',
                'verbose_name_plural': 'Covers',
            },
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='avatar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diventiuser', to='accounts.DiventiAvatar', verbose_name='avatar'),
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.DiventiCover', verbose_name='cover'),
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='diventiuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
