# Generated by Django 2.1.7 on 2019-05-12 14:04

from django.db import migrations
from django.utils.text import slugify


def forwards(apps, schema_editor):
    user_model = apps.get_model('accounts', 'DiventiUser')
    for obj in user_model.objects.all():
        if not obj.nametag:
            obj.nametag = '-'.join((slugify(obj.first_name), slugify(obj.pk)))
            if obj.is_staff == False:
                obj.profilepic = None
            else:
                obj.role = None
            print(obj.first_name)
            obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0135_auto_20190512_1602'),
    ]

    operations = [
        migrations.RunPython(
            forwards, 
            reverse_code=migrations.RunPython.noop
        ),
    ]