# Generated by Django 2.0.8 on 2018-10-04 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0057_remove_section_diventicard'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='section', to='homebrew.Card', verbose_name='card'),
        ),
    ]