# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0006_auto_20150320_1305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['-date', '-page_number'], 'verbose_name_plural': 'entries'},
        ),
        migrations.AlterModelOptions(
            name='folder',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='reading',
            options={'ordering': ['order', 'started_date']},
        ),
        migrations.AddField(
            model_name='entry',
            name='num_pages',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='reading',
            field=models.ForeignKey(to='bookshelf.Reading', related_name='entries'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reading',
            name='folder',
            field=models.ForeignKey(blank=True, to='bookshelf.Folder', related_name='readings', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reading',
            name='started_date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
