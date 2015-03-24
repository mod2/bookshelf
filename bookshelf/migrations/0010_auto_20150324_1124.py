# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0009_auto_20150324_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='started_date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
