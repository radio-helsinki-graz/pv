# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_host_is_always_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active', editable=False),
        ),
    ]
