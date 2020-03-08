# Generated by Django 2.2.10 on 2020-03-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_auto_20200304_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='meta_category',
            field=models.BooleanField(default=False, help_text="Meta categories won't be listed in search results, nor on reporting pages.", verbose_name='meta category'),
        ),
    ]
