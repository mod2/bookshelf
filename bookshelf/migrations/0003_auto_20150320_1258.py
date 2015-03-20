# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookshelf', '0002_auto_20150320_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reading',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=True,
        ),
    ]
