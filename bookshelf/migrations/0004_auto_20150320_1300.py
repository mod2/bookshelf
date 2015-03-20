# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0003_auto_20150320_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date_published',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(max_length=10, choices=[('active', 'Active'), ('deleted', 'Deleted')], default='active'),
            preserve_default=True,
        ),
    ]
