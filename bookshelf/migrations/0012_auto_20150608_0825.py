# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0011_auto_20150608_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='stale_period',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
