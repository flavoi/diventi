# Generated by Django 2.2.10 on 2020-02-29 15:00

import diventi.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0256_auto_20200229_1555'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='diventiuser',
            managers=[
                ('objects', diventi.accounts.models.DiventiUserManager()),
            ],
        ),
    ]