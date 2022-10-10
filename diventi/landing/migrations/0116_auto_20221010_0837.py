# Generated by Django 2.2.28 on 2022-10-10 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0077_auto_20220917_1035'),
        ('landing', '0115_auto_20221009_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutarticle',
            options={'verbose_name': 'about article', 'verbose_name_plural': 'about articles'},
        ),
        migrations.AddField(
            model_name='section',
            name='attached_product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product', verbose_name='product'),
        ),
    ]
