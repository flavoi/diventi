# Generated by Django 2.2.12 on 2020-05-03 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0015_auto_20200503_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resolution',
            name='antagonist_goal',
        ),
        migrations.AddField(
            model_name='resolution',
            name='antagonist_goals',
            field=models.ManyToManyField(blank=True, to='adventures.AntagonistGoal', verbose_name='antagonist goal'),
        ),
    ]