# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0005_auto_20150320_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='finished_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reading',
            name='goal_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reading',
            name='started_date',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
