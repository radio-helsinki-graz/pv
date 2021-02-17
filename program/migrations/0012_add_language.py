# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0011_programslot_remove_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('native_name', models.CharField(max_length=32, verbose_name='Native Name')),
            ],
            options={
                'ordering': ('language',),
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.AddField(
            model_name='show',
            name='language',
            field=models.ManyToManyField(related_name='language', verbose_name='Language', to='program.Language', blank=True),
        ),
    ]
