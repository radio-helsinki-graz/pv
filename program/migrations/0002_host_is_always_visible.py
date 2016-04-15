# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='is_always_visible',
            field=models.BooleanField(default=False, verbose_name='Is always visible'),
        ),
    ]
