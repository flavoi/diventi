# Generated by Django 2.2.16 on 2020-10-05 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0119_auto_20201005_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='logo_background',
            field=models.CharField(choices=[('light-secondary', 'dark-secondary'), ('secondary', 'secondary'), ('dark-secondary', 'dark-secondary'), ('light-primary', 'light-primary'), ('primary', 'primary'), ('dark-primary', 'dark-primary'), ('light-dark', 'light-dark'), ('dark', 'dark'), ('dark-dark', 'dark-dark'), ('light-success', 'light-success'), ('success', 'success'), ('dark-success', 'dark-success'), ('light-danger', 'light-danger'), ('danger', 'danger'), ('dark-danger', 'dark-danger'), ('light-warning', 'light-warning'), ('warning', 'warning'), ('dark-warning', 'dark-warning'), ('light-info', 'light-info'), ('info', 'info'), ('dark-info', 'dark-info')], default='secondary', max_length=30, verbose_name='logo background'),
        ),
    ]