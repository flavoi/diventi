# Generated by Django 2.2.1 on 2019-06-03 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0043_auto_20190531_0751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='category',
        ),
        migrations.DeleteModel(
            name='SectionCategory',
        ),
    ]
