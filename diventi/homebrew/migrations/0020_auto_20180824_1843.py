# Generated by Django 2.0.8 on 2018-08-24 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0019_section_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='new_page',
            field=models.BooleanField(default=False, verbose_name='new page'),
        ),
        migrations.AlterField(
            model_name='dicetablerow',
            name='dicetable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='homebrew.DiceTable'),
        ),
    ]
