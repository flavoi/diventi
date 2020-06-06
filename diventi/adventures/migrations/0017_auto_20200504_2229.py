# Generated by Django 2.2.12 on 2020-05-04 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventures', '0016_auto_20200503_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resolution',
            name='antagonist_goals',
        ),
        migrations.RemoveField(
            model_name='situation',
            name='resolution',
        ),
        migrations.AddField(
            model_name='antagonistgoal',
            name='situations',
            field=models.ManyToManyField(through='adventures.Resolution', to='adventures.Situation', verbose_name='situations'),
        ),
        migrations.AddField(
            model_name='resolution',
            name='antagonist_goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adventures.AntagonistGoal', verbose_name='antagonist goal'),
        ),
        migrations.AddField(
            model_name='resolution',
            name='situation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adventures.Situation', verbose_name='situation'),
        ),
    ]