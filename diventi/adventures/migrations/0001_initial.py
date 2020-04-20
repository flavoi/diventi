# Generated by Django 2.2.12 on 2020-04-20 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0040_auto_20200308_1655'),
        ('ebooks', '0097_auto_20200419_2307'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adventure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('icon', models.CharField(blank=True, max_length=30, verbose_name='icon')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='warning', max_length=30, verbose_name='color')),
                ('ring', models.CharField(choices=[('first', 'First'), ('second', 'Second'), ('third', 'Third')], max_length=20, verbose_name='ring of storytelling')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adventures', to='products.Product', verbose_name='product')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adventures', to='ebooks.Section', verbose_name='section')),
            ],
            options={
                'verbose_name': 'Adventure',
                'verbose_name_plural': 'Adventures',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='customer')),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('title_it', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=50, null=True, verbose_name='title')),
                ('icon', models.CharField(blank=True, max_length=30, verbose_name='icon')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('color', models.CharField(blank=True, choices=[('info', 'Blue'), ('primary', 'Rose'), ('danger', 'Red'), ('warning', 'Yellow'), ('success', 'Green'), ('default', 'Gray')], default='warning', max_length=30, verbose_name='color')),
            ],
            options={
                'verbose_name': 'Resolution',
                'verbose_name_plural': 'Resolutions',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('players', models.ManyToManyField(through='adventures.Match', to=settings.AUTH_USER_MODEL, verbose_name='players')),
            ],
            options={
                'verbose_name': 'Story',
                'verbose_name_plural': 'Stories',
            },
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('adventure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='situations', to='adventures.Adventure', verbose_name='adventure')),
                ('game_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='situations', to=settings.AUTH_USER_MODEL, verbose_name='game master')),
                ('next_situation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adventures.Situation', verbose_name='next situation')),
                ('resolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='situations', to='adventures.Resolution', verbose_name='resolution')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='situation', to='adventures.Story', verbose_name='story')),
            ],
            options={
                'verbose_name': 'Situation',
                'verbose_name_plural': 'Situations',
            },
        ),
        migrations.AddField(
            model_name='match',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adventures.Story', verbose_name='story'),
        ),
    ]
