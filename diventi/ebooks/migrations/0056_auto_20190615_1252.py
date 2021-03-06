# Generated by Django 2.2.2 on 2019-06-15 10:51

from django.db import migrations, models, transaction, IntegrityError
from django.template.defaultfilters import slugify


def forwards_it(apps, schema_editor):
    user_model = apps.get_model('ebooks', 'Section')
    for obj in user_model.objects.all():
        print('Generating slug for it instance of {0}'.format(obj))
        try:
            with transaction.atomic():
                obj.slug_it = slugify(obj.title_it)
                obj.save()
        except IntegrityError:
            pass

def forwards_en(apps, schema_editor):
    user_model = apps.get_model('ebooks', 'Section')
    for obj in user_model.objects.all():
        print('Generating slug for en instance of {0}'.format(obj))
        try:
            with transaction.atomic():
                obj.slug_en = slugify(obj.title_en)
                obj.save()
        except IntegrityError:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0055_auto_20190615_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=models.SlugField(null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='section',
            name='slug_en',
            field=models.SlugField(null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='section',
            name='slug_it',
            field=models.SlugField(null=True, verbose_name='slug'),
        ),
        migrations.RunPython(
            forwards_it,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            forwards_en,
            reverse_code=migrations.RunPython.noop
        ),
    ]
