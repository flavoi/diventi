# Generated by Django 2.0.8 on 2018-10-26 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0022_question__type'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='title')),
                ('title_it', models.CharField(max_length=60, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=60, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_it', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('score', models.PositiveIntegerField(blank=True, verbose_name='score')),
            ],
            options={
                'verbose_name': 'choice',
                'verbose_name_plural': 'choices',
            },
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'verbose_name': 'survey', 'verbose_name_plural': 'surveys'},
        ),
        migrations.AlterModelOptions(
            name='surveycover',
            options={'verbose_name': 'survey cover', 'verbose_name_plural': 'survey covers'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='_type',
        ),
        migrations.AddField(
            model_name='questionchoice',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='feedbacks.Question'),
        ),
    ]