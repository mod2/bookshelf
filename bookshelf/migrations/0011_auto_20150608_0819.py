# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0010_auto_20150324_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='stale_period',
            field=models.PositiveSmallIntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
