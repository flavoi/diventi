# Generated by Django 2.2.12 on 2020-05-04 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0017_auto_20200504_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='antagonistgoal',
            name='situations',
        ),
        migrations.RemoveField(
            model_name='resolution',
            name='antagonist_goal',
        ),
        migrations.RemoveField(
            model_name='resolution',
            name='situation',
        ),
        migrations.AddField(
            model_name='resolution',
            name='antagonist_goals',
            field=models.ManyToManyField(blank=True, to='adventures.AntagonistGoal', verbose_name='antagonist goal'),
        ),
        migrations.AddField(
            model_name='situation',
            name='resolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='situations', to='adventures.Resolution', verbose_name='resolution'),
        ),
    ]
