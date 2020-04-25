# Generated by Django 2.2.12 on 2020-04-25 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventure',
            name='ring',
            field=models.CharField(choices=[('first', 'First Ring'), ('second', 'Second Ring'), ('third', 'Third Ring')], max_length=20, verbose_name='ring of storytelling'),
        ),
        migrations.AlterField(
            model_name='situation',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='situations', to='adventures.Story', verbose_name='story'),
        ),
    ]
