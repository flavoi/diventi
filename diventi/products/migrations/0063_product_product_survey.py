# Generated by Django 2.2.16 on 2020-10-24 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0043_auto_20200825_2300'),
        ('products', '0062_product_unfolded'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='feedbacks.Survey', verbose_name='survey'),
        ),
    ]
