# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0004_auto_20150320_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date_published',
            field=models.CharField(blank=True, max_length=100, null=True),
            preserve_default=True,
        ),
    ]
