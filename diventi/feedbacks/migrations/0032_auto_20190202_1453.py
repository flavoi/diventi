# Generated by Django 2.1.5 on 2019-02-02 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0031_auto_20181028_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='outcome',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='survey', to='feedbacks.Outcome', verbose_name='outcome'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question_groups',
            field=models.ManyToManyField(related_name='surveys', to='feedbacks.QuestionGroup', verbose_name='question groups'),
        ),
    ]
