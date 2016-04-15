# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0003_host_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active', editable=False),
        ),
    ]
