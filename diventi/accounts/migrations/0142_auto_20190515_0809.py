# Generated by Django 2.1.7 on 2019-05-15 06:09

import diventi.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0141_auto_20190515_0744'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='diventiuser',
            managers=[
                ('objects', diventi.accounts.models.DiventiUserManager()),
            ],
        ),
    ]
