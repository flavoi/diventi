# Generated by Django 2.2.2 on 2019-06-20 10:18

import diventi.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0208_auto_20190619_0824'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='diventiuser',
            managers=[
                ('objects', diventi.accounts.models.DiventiUserManager()),
            ],
        ),
    ]