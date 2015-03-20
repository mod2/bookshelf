# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('author', models.CharField(null=True, blank=True, max_length=400)),
                ('status', models.CharField(choices=[('active', 'Active'), ('deleted', 'Deleted')], max_length=10)),
                ('date_published', models.DateTimeField(null=True, blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('isbn', models.CharField(null=True, blank=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('page_number', models.PositiveSmallIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['page_number', '-date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('order', models.PositiveSmallIntegerField(default=100)),
                ('color', models.CharField(null=True, blank=True, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('status', models.CharField(default='active', choices=[('active', 'Active'), ('finished', 'Finished'), ('abandoned', 'Abandoned'), ('deleted', 'Deleted')], max_length=10)),
                ('started_date', models.DateTimeField(auto_now_add=True)),
                ('goal_date', models.DateTimeField(null=True, blank=True)),
                ('finished_date', models.DateTimeField(null=True, blank=True)),
                ('start_page', models.PositiveSmallIntegerField(default=1)),
                ('end_page', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('order', models.PositiveSmallIntegerField(default=100)),
                ('book', models.ForeignKey(to='bookshelf.Book')),
                ('folder', models.ForeignKey(null=True, blank=True, to='bookshelf.Folder')),
            ],
            options={
                'ordering': ['started_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('color', models.CharField(null=True, blank=True, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reading',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, to='bookshelf.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='reading',
            field=models.ForeignKey(to='bookshelf.Reading'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(null=True, blank=True, to='bookshelf.Tag'),
            preserve_default=True,
        ),
    ]
