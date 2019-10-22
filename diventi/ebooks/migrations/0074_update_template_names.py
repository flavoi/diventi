# Generated by Django 2.2.3 on 2019-08-07 06:48

from django.db import migrations, models

def forwards(apps, schema_editor):
    user_model = apps.get_model('ebooks', 'Section')
    obj = user_model.objects.all()
    DEFAULT_TEMPLATE = 'section_standard'
    obj.update(template=DEFAULT_TEMPLATE)     

class Migration(migrations.Migration):

    dependencies = [
        ('ebooks', '0073_auto_20190807_0840'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            reverse_code=migrations.RunPython.noop
        ),
    ]