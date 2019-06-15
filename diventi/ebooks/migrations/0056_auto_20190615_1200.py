# Generated by Django 2.2.2 on 2019-06-15 09:47

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
        ('ebooks', '0055_add_slug_to_sections'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='slug_en',
            field=models.SlugField(null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='section',
            name='slug_it',
            field=models.SlugField(null=True, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='section',
            name='card_type',
            field=models.CharField(choices=[(' ', 'Standard'), ('card-plain', 'No background')], default=' ', max_length=30, verbose_name='card type'),
        ),
        migrations.AlterField(
            model_name='section',
            name='template',
            field=models.CharField(choices=[('section_standard.html', 'Standard'), ('section_with_icon.html', 'With icon'), ('section_with_image.html', 'With image')], default='section_standard.html', max_length=50, verbose_name='template'),
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
