# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0004_show_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='programslot',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active', editable=False),
        ),
    ]
