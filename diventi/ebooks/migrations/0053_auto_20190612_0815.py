# Generated by Django 2.2.1 on 2019-06-12 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0052_auto_20190612_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='card_type',
            field=models.CharField(choices=[(' ', 'normal'), ('card-plain', 'plain'), ('card-testimonial', 'testimonial')], default=' ', max_length=30, verbose_name='card type'),
        ),
    ]