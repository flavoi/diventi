# Generated by Django 2.0.8 on 2018-08-25 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0029_auto_20180825_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='_list',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='section', to='homebrew.Itemize'),
        ),
    ]
