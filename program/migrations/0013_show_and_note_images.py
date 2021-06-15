# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import program.models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0012_add_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='show',
            name='image_enabled',
        ),
        migrations.AlterField(
            model_name='show',
            name='image',
            field=models.ImageField(max_length=350, upload_to=program.models.show_image_filename, null=True, verbose_name='Image', blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='image',
            field=models.ImageField(max_length=350, upload_to=program.models.note_image_filename, null=True, verbose_name='Image', blank=True),
        ),
    ]
