# Generated by Django 2.2.3 on 2019-08-07 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0072_auto_20190805_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='template',
            field=models.CharField(choices=[('section_standard', 'Standard'), ('section_with_icon', 'With icon'), ('section_with_image', 'With image')], default='section_standard', max_length=50, verbose_name='template'),
        ),
    ]
