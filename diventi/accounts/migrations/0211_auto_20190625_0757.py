# Generated by Django 2.2.2 on 2019-06-25 05:57

import diventi.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0210_auto_20190620_1220'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='diventiuser',
            managers=[
                ('objects', diventi.accounts.models.DiventiUserManager()),
            ],
        ),
    ]
